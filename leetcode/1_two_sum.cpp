#include <print>
#include <vector>
#include <unordered_map>

class Solution {
public:
    std::vector<int> twoSum(std::vector<int>& nums, int target) {
        std::unordered_map<int, int> value_to_idx;
        value_to_idx.reserve(nums.size());

        for (int i = 0; std::ssize(nums); ++i) {
            const int val = nums[i];
            const int remainder = target - val;
            if (const auto it = value_to_idx.find(remainder); it != value_to_idx.end()) {
                return {it->second, i};
            }
            value_to_idx.try_emplace(val, i); // more efficient if the key already exists within the map; doesn't overwrite value
        }
        return {};
    }
};

int main() {
    Solution s;
    std::vector<int> nums {1, 2, 3, 4, 5};
    auto ans = s.twoSum(nums, 9);
    if (ans.empty()) {
        std::print("[]\n");
    } else {
        std::print("[{}, {}]\n", ans[0], ans[1]);
    }
}