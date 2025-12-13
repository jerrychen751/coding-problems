from typing import List

class Solution:
    # DP Approach
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        # We seek to find the longest subsequence of values where prev_end <= curr_start
        # Maintain dp array where dp[i] is the length of the longest subsequence ending at i
        intervals.sort(key=lambda x: x[0])
        n = len(intervals)
        dp = [1] * n
        for i in range(1, n):
            for j in range(i):
                if intervals[i][0] >= intervals[j][1]:
                    dp[i] = max(dp[i], dp[j] + 1)

        return n - max(dp)
    
    # Greedy Approach
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        # Initially, the thought is "What should I remove to minimize overlaps --> remove interval with highest number of overlap first"
        # But this leads to dynamic updates for all other intervals with some shared overlap
        # Instead we want to maximize the number of intervals kept
        # The solution is to not need to care about other intervals; there's not even a need to compare any interval to more than one other interval
        # Instead, the interval with the shortest ending time is always going to be the optimal choice to keep. Even if another interval may start later or be shorter, as long as it overlaps with an earlier ending time it should be removed (always better to keep earlier end)

        intervals.sort(key=lambda x: x[1])
        last_interval = intervals[0]
        removed_ct = 0
        for i in range(1, len(intervals)):
            curr_interval = intervals[i]
            if curr_interval[0] < last_interval[1]:
                removed_ct += 1
                continue
            last_interval = curr_interval
        
        return removed_ct        
        
    
if __name__ == '__main__':
    s = Solution()
    print(s.eraseOverlapIntervals([[0,2], [1,3], [1,3], [2,4], [3,5], [3,5], [4,6]]))