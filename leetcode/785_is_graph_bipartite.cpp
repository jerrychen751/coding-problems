#include <vector>
#include <deque>

class Solution {
public:
    bool isBipartite(std::vector<std::vector<int>>& graph) {
        // Store 3 states for node: unvisited, in group A, in group B
        size_t n = graph.size();
        std::vector<char> partition(n, '0'); // '0' for unvisited, '1' for group A, '2' for group B

        for (size_t i = 0; i < n; ++i) {
            if (partition[i] != '0') {
                continue; // start from clean slate; no need to process an already-grouped node
            }

            partition[i] = '1';
            std::deque<int> queue;
            queue.push_back(static_cast<int>(i));
            while (!queue.empty()) {
                const int node = queue.front();
                queue.pop_front();

                // Process neighbors
                for (const int neighbor : graph[node]) {
                    if (partition[neighbor] == '0') {
                        partition[neighbor] = (partition[node] == '1') ? '2' : '1';
                        queue.push_back(neighbor);
                    } else if (partition[neighbor] == partition[node]) {
                        return false;
                    }
                }
            }
        }

        return true;
    }
};