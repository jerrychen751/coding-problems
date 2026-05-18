from typing import List


class Solution:
    def intersectionSizeTwo(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda x:(x[1], -x[0])) # for intervals with same end, let the smaller interval come first
        # This way, we never hit case 2 where the element we're adding is not new (when two intervals share the same end)
        set_size = 0 # instead of tracking the set itself, just increment counter and track the latest 2 elements added

        # Set up the initial interval
        n1, n2 = intervals[0][-1] - 1, intervals[0][-1]
        set_size += 2
        for i in range(1, len(intervals)):
            s, e = intervals[i]

            # Case 1: we can reuse what we have before
            if s <= n1:
                continue

            # Case 2: we can reuse one number we have before
            if s <= n2:
                set_size += 1
                n1 = n2 # reuse old n2
                n2 = e # taking the end of the interval is always optimal; makes it easier for next interavl to contain new n2
            # Case 3: unable to reuse
            else:
                set_size += 2
                n1, n2 = e - 1, e

        return set_size
