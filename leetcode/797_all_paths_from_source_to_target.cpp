// https://leetcode.com/problems/all-paths-from-source-to-target/description/?envType=problem-list-v2&envId=graph

#include <vector>

namespace DP {
    class Solution {
    public:
        std::vector<std::vector<int>> allPathsSourceTarget(std::vector<std::vector<int>>& graph) {
            const int n = static_cast<int>(graph.size());
            std::vector<std::vector<std::vector<int>>> dp(n);
            std::vector<bool> visited(n, false);

            auto dfs = [&] (auto&& self, int curr) -> const std::vector<std::vector<int>> {
                if (visited[curr]) {
                    return dp[curr];
                }
                visited[curr] = true;

                if (curr == n - 1) {
                    dp.back() = {{n - 1}};
                    return dp.back();
                }

                for (int neighbor : graph[curr]) {
                    const auto& child_paths = self(self, neighbor);
                    for (const auto& p : child_paths) {
                        std::vector<int> path;
                        path.reserve(p.size() + 1);
                        path.push_back(curr);
                        path.insert(path.end(), p.begin(), p.end());
                        dp[curr].push_back(path);
                    }
                }

                return dp[curr];
            };

            return dfs(dfs, 0);
        }
    };
}

namespace Backtracking {
    class Solution {
    public:
        std::vector<std::vector<int>> allPathsSourceTarget(std::vector<std::vector<int>>& graph) {
            const int n = static_cast<int>(graph.size());
            if (n == 0) {
                return {};
            }
            
            std::vector<std::vector<int>> res;
            std::vector<int> path;
            path.reserve(n);
            path.push_back(0);

            auto dfs = [&] (auto&& self, int idx) {
                if (idx == n - 1) {
                    res.push_back(path); // make copy of path
                    return;
                }

                for (int neighbor : graph[idx]) {
                    path.push_back(neighbor);
                    self(self, neighbor);
                    path.pop_back();
                }
            };

            dfs(dfs, 0);
            return res;
        }
    };
}