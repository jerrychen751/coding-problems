#include <vector>

class Solution {
public:
    int minTime(int n, std::vector<std::vector<int>>& edges, std::vector<bool>& hasApple) {
        std::vector<std::vector<int>> graph(n);
        for (const auto& edge : edges) {
            int source = edge[0];
            int dest = edge[1];
            graph[source].push_back(dest);
            graph[dest].push_back(source);
        }

        return dfs(graph, hasApple, 0, 0);
    }

private:
    int dfs(
        std::vector<std::vector<int>>& graph, 
        std::vector<bool>& hasApple, 
        int node,
        int parent
    ) {
        int time = 0; // return time to collect all of this subtree's apples

        for (int neighbor : graph[node]) {
            if (neighbor == parent) {
                continue;
            }

            int child_time = dfs(graph, hasApple, neighbor, node);
            if (hasApple[neighbor] || child_time > 0) {
                time += child_time + 2; // need to travel to child and back from curr node
            }
        }

        return time;
    }
};
