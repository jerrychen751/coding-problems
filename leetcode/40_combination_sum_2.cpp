#include <vector>
#include <algorithm>
#include <print>


class Solution {
public:
    std::vector<std::vector<int>> combinationSum2(std::vector<int>& candidates, int target) {
        std::ranges::sort(candidates);
        int curr_idx = 0;
        std::vector<int> combination;
        std::vector<std::vector<int>> res;

        backtrack(target, combination, 0, candidates, res);

        return res;
    }

private:
    void backtrack(
        int remaining,
        std::vector<int>& combination,
        int curr_idx,
        const std::vector<int>& candidates,
        std::vector<std::vector<int>>& res
    ) {
        if (remaining == 0) {
            res.push_back(combination);
            return;
        }

        for (int i = curr_idx; i < static_cast<int>(candidates.size()); ++i) {
            if (i > curr_idx && candidates[i] == candidates[i - 1]) {
                continue;
            }

            int num = candidates[i];

            if (num > remaining) {
                break;
            }

            combination.push_back(num);
            backtrack(remaining - num, combination, i + 1, candidates, res);
            combination.pop_back();
        }
    }
};

int main() {
    Solution s;
    std::vector<int> candidates = {2, 5, 2, 1, 2};
    std::print("{}", s.combinationSum2(candidates, 5));
}
