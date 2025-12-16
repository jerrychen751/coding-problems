#include <vector>
#include <algorithm>
#include <print>

class Solution {
public:
    int coinChange(std::vector<int>& coins, int amount) {
        // dp[i] represents fewest number of coins to reach i amount of money
        std::vector<int> dp(amount + 1, amount + 1);
        dp[0] = 0;
        for (int i = 1; i < dp.size(); ++i) {
            for (int coin : coins) {
                if (i - coin >= 0 && dp[i - coin] != amount + 1) { // only consider if 
                    dp[i] = std::min(dp[i], dp[i - coin] + 1);
                }
            }
        }

        if (dp[amount] == amount + 1) {
            return -1;
        }
        return dp[amount];
    }
};

int main() {
    Solution s;
    std::vector<int> coins = {1, 2, 5};
    std::println("{}", s.coinChange(coins, 11));
}