#include <vector>
#include <print>

class Solution {
public:
    int repeatedNTimes(std::vector<int>& nums) {
        int n = nums.size();
        for (size_t dist = 1; dist < 4; ++dist) {
            for (size_t i = 0; i < n - dist; ++i) {
                if (nums[i] == nums[i + dist]) {
                    return nums[i];
                }
            }
        }
        
        return -1;
    }
};

int main() {
    std::vector<int> nums {1, 2, 3, 3};
    Solution s;
    std::print("{}", s.repeatedNTimes(nums));
}