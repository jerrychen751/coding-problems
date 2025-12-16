#include <algorithm>
#include <vector>
#include <print>

namespace DP {
    class Solution {
    public:
        int uniquePaths(int m, int n) {
            std::vector<int> row(n, 1);

            for (int i = 1; i < m; ++i) {
                for (int j = 1; j < n; ++j) {
                    row[j] += row[j - 1];
                }
            }
            return row[n - 1];
        }
    };
}

namespace Math {
    class Solution {
    public:
        int uniquePaths(int m, int n) {
            int N = m + n - 2;
            int R = std::min(m - 1, n - 1);
            unsigned long long res = 1;

            for (int i = 1; i <= R; ++i) {
                res = res * (N - i + 1) / i;
            }
            return (int)res;
        }
    };
}

int main() {
    DP::Solution dp;
    std::println("DP Solution (3, 7): {}", dp.uniquePaths(3, 7));

    Math::Solution math;
    std::println("Math Solution (3, 7): {}", math.uniquePaths(3, 7));

    return 0;
}