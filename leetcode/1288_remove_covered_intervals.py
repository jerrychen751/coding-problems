from typing import List

class Solution:
    def removeCoveredIntervals(self, intervals: List[List[int]]) -> int:
        # interval[i] is a list of size 2; start is inclusive, end is exclusive
        # condition for [c, d) covering [a, b): c <= a and d >= b
        # return number of intervals; i.e., any interval covered by another is not included

        # is it possible for start/end of interval to be the same? invalid intervals?

        # sorting
        # [[1, 4], [2, 8], [3, 6]]
        # max_end -> idx 0 would have max_end=4
        # max_end -> 8
        # curr_end <= max_end -> increment counter

        # [[1, 2], [1, 3], [1, 4], [1, 5], [2, 6]]

        if not intervals:
            return 0

        def comparator(interval: List[int]) -> tuple[int, int]:
            return interval[0], -interval[1]
        
        intervals.sort(key=comparator)
        covered_ct = 0
        max_end = intervals[0][-1]
        for i in range(1, len(intervals)):
            start, end = intervals[i]
            if end <= max_end:
                covered_ct += 1
            else: # guaranteed to be a different start index
                max_end = end

        return len(intervals) - covered_ct

        # after sorting, we have [[1, 4], [2, 8], [3, 6]]
        # at first, we have max_end = 4
        # start=2, end=8 -> max_end = 8
        # start=3, end=6 -> max_end = 8 -> covered_ct = 1