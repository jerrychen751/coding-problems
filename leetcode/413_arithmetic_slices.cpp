#include <vector>
#include <print>

class Solution {
public:
    int numberOfArithmeticSlices(std::vector<int>& nums) {
        if (nums.size() <= 2) {
            return 0;
        }
        
        int res = 0;
        int length = 0;

        for (size_t i = 2; i < nums.size(); ++i) {
            int diff1 = nums[i - 1] - nums[i - 2];
            int diff2 = nums[i] - nums[i - 1];
            if (diff1 == diff2) {
                ++length;
                res += length;
            } else {
                length = 0;
            }
        }

        return res;
    }
};

int main() {
    std::vector<int> nums {1, 2, 3, 4};
    Solution s;
    std::print("{}", s.numberOfArithmeticSlices(nums));
}