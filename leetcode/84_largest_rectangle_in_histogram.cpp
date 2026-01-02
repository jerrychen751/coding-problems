#include <vector>
#include <algorithm>
#include <print>

class Solution {
public:
    int largestRectangleArea(std::vector<int>& heights) {
        // Maintain a stack, keeping track of historical (idx, height)
        // If the new bar decreases or is equal in height, then all bars in stack taller must be popped
        // (cannot continue at their original heights)
        // Then add to stack as (last_popped_idx, height)

        // If the new bar increases in height, add it to the stack
        std::vector<std::pair<int, int>> stack;
        int max_area = 0;
        const int n = static_cast<int>(heights.size());

        for (int idx = 0; idx < n; ++idx) {
            int start = idx;
            const auto height = heights[idx];

            while (!stack.empty() && height <= stack.back().second) {
                const auto [prev_idx, prev_height] = stack.back();
                stack.pop_back();

                max_area = std::max(max_area, prev_height * (static_cast<int>(idx) - prev_idx));
                start = prev_idx;
            }

            stack.emplace_back(start, height);
        }

        // Deal with the remaining elements in the stack after reaching end of heights
        // Occurs if ending is monotonically increasing
        while (!stack.empty()) {
            const auto [idx, height] = stack.back();
            stack.pop_back();
            max_area = std::max(max_area, height * (n - idx));
        }

        return max_area;
    }
};

int main() {
    std::vector<int> heights {2, 1, 5, 6, 2, 3};
    Solution s;
    std::print("{}", s.largestRectangleArea(heights));
}