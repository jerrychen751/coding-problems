from typing import List


class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        # Two intervals are overlapping if s2 <= e1, when they are sorted in ascending order by end time
        intervals.sort(key=lambda x:(x[1], x[0]))
        res = []
        for interval in intervals:
            s, e = interval
            while len(res) > 0 and res[-1][1] >= s:
                prev_interval = res.pop()
                s = min(s, prev_interval[0]) # e is guaranteed to be >= prev_interval[1]
                # we use a while loop because although prev_interval[0] > earlier interval end times, the same cannot be said for
                # interval[0]

            res.append((s, e))

        return res
