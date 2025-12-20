#include <algorithm>
#include <vector>
#include <print>

namespace DP {
    class Solution {
    public:
        int eraseOverlapIntervals(std::vector<std::vector<int>>& intervals) {
            std::sort(intervals.begin(), intervals.end(), [](const auto& a, const auto& b) {
                return a.front() < b.front();
            });
            int n = intervals.size();
            std::vector<int> dp(n, 1);
            for (int i = 1; i < n; ++i) {
                for (int j = 0; j < i; ++j) {
                    if (intervals[i][0] >= intervals[j][1]) {
                        dp[i] = std::max(dp[i], dp[j] + 1);
                    }
                }
            }
            // fewest amount of intervals erased = total - length of longest subsequence
            return n - std::ranges::max(dp);
        }
    };
}

namespace Greedy {
    class Solution {
    public:
        int eraseOverlapIntervals(std::vector<std::vector<int>>& intervals) {
            if (intervals.empty()) {
                return 0;
            }

            std::sort(intervals.begin(), intervals.end(), [](const auto& a, const auto& b) {
                return a.back() < b.back();
            });

            int last_end = intervals.front().back(); // end time of last kept interval
            int removed_ct = 0;
            for (std::size_t i = 1; i < intervals.size(); ++i) {
                if (intervals[i].front() < last_end) {
                    ++removed_ct;
                } else {
                    last_end = intervals[i].back();
                }
            }

            return removed_ct;
        }
    };
}

int main() {
    Greedy::Solution s;
    std::vector<std::vector<int>> intervals {{1, 3}, {2, 4}, {3, 6}};
    std::print("{}", s.eraseOverlapIntervals(intervals));
}