#include <vector>
#include <algorithm>
#include <ranges>
#include <print>

class Solution {
public:
    std::vector<std::vector<int>> combinationSum(std::vector<int>& candidates, int target) {
        std::ranges::sort(candidates);
        auto new_end = std::ranges::unique(candidates).begin();
        candidates.erase(new_end, candidates.end());

        std::vector<std::vector<int>> res;
        std::vector<int> combination;
        backtrack(target, combination, 0, candidates, res);
        return res;
    }

private:
    void backtrack(
        int remaining,
        std::vector<int>& combination,
        int curr_idx,
        std::vector<int>& candidates,
        std::vector<std::vector<int>>& res
    ) {
        if (remaining == 0) {
            res.push_back(combination);
            return;
        }

        for (int i = curr_idx; i < static_cast<int>(candidates.size()); ++i) {
            int num = candidates[i];
            if (remaining - num < 0) {
                break; // prune; don't check rest because we know by sorted order, they will only be larger and continue leading to invalid sums
            }

            combination.push_back(num);
            backtrack(remaining - num, combination, i, candidates, res);
            combination.pop_back();
        }
    }
};

int main() {
    Solution s;
    std::vector<int> candidates {2, 3, 6, 7};
    std::print("{}", s.combinationSum(candidates, 7));
}