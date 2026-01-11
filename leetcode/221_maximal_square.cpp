#include <algorithm>
#include <vector>

class Solution {
public:
    int maximalSquare(std::vector<std::vector<char>>& matrix) {
        if (matrix.empty()) {
            return 0;
        }

        int m = static_cast<int>(matrix.size());
        int n = static_cast<int>(matrix[0].size());
        int max_side_length = 0;
        std::vector<int> dp(n, 0);

        for (int i = m - 1; i >= 0; --i) {
            int diag = 0;
            for (int j = 0; j < n; ++j) {
                int left = (j - 1 < 0) ? 0 : dp[j - 1];
                int bottom = dp[j];
                if (matrix[i][j] == '1') {
                    // We are consistently limited by the smallest of the 3: left, bottom, diag
                    int side_length = std::min({left, bottom, diag});
                    dp[j] = side_length + 1;
                } else {
                    dp[j] = 0;
                }
                diag = bottom;
                max_side_length = std::max(max_side_length, dp[j]);
            }
        }
        return max_side_length * max_side_length;
    }
};