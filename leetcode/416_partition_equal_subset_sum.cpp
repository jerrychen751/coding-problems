#include <numeric>
#include <print>
#include <vector>

class Solution {
public:
    bool canPartition(std::vector<int> nums) {
        int total = std::accumulate(nums.begin(), nums.end(), 0);
        if (total % 2 == 1) {
            return false;
        }

        int target = total / 2;
        std::vector<bool> dp(target + 1, false); // dp[i] means whether there exists a partition summing to i
        dp[0] = true;
        for (int num : nums) {
            for (int i = target; i >= num; --i) {
                dp[i] = dp[i] || dp[i - num];
            }
        }

        return dp[target];
    }
};

int main() {
    std::vector<int> nums {1, 5, 11, 5};
    Solution s;
    std::print("{}", s.canPartition(nums));
}