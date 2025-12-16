#include <print>
#include <vector>
#include <algorithm>

class Solution {
public:
    int wiggleMaxLength(std::vector<int>& nums) {
        int n = nums.size();
        if (n < 2) {
            return n;
        }

        int max_subseq_up = 1;
        int max_subseq_down = 1;
        for (int i = 1; i < n; ++i) {
            int delta = nums[i] - nums[i - 1];
            if (delta < 0) {
                max_subseq_down = max_subseq_up + 1;
            } else if (delta > 0) {
                max_subseq_up = max_subseq_down + 1;
            }
        }

        return std::max(max_subseq_down, max_subseq_up);
    }
};

int main() {
    Solution s;
    std::vector<int> nums = {1, 7, 4, 9, 2, 5};
    std::print("{}", s.wiggleMaxLength(nums));
}