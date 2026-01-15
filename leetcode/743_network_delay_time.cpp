#include <vector>
#include <queue>
#include <limits>
#include <algorithm>

class Solution {
public:
    int networkDelayTime(std::vector<std::vector<int>>& times, int n, int k) {
        // Non-negative edge weights
        std::vector<std::vector<std::pair<int, int>>> graph(n + 1); // 1-indexed
        for (const auto& time : times) {
            int u = time[0];
            int v = time[1];
            int w = time[2];
            graph[u].emplace_back(v, w);
        }
        const int INF = std::numeric_limits<int>::max();
        std::vector<int> dists(n + 1, INF); // store distances for each node
        // if none are inf, that means we can reach all and return sum; otherwise return -1
        dists[k] = 0; // start

        std::priority_queue<
            std::pair<int, int>,
            std::vector<std::pair<int, int>>,
            std::greater<std::pair<int, int>>
        > pq;
        pq.emplace(0, k);

        while (!pq.empty()) {
            auto [d, u] = pq.top();
            pq.pop();

            if (d > dists[u]) { // can only be >=
                continue;
            }

            for (auto [v, w] : graph[u]) {
                if ((d != INF) && (d + w < dists[v])) {
                    dists[v] = d + w;
                    pq.emplace(dists[v], v);
                }
            }
        }

        int res = 0;
        for (size_t i = 1; i < dists.size(); ++i) {
            if (dists[i] == INF) {
                return -1;
            }
            res = std::max(res, dists[i]);
        }
        return res;
    }
};