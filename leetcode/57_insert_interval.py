from typing import List


class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        # intervals is sorted sorter by start, non overlapping initially
        # after inserting newInterval, we merge any overlaps (inclusive points) and return new intervals list with the merged interval

        # what counts as overlapping? comparing interval to newInterval, they do NOT overlap if
        # interval[0] > newInterval[1] (interval to right of newInterval) or interval[1] < newInterval[0] (interval left of newInterval)
        # flipping these, they overlap if interval[0] <= newInterval[1] and interval[1] >= newInterval[0]

        def is_overlapping(interval1: list[int], interval2: list[int]) -> bool:
            return interval1[0] <= interval2[1] and interval1[1] >= interval2[0]

        merged_intervals = []
        for interval in intervals:
            # 2 cases: either they don't overlap (append interval; no merge) or they do and we keep the smaller of the starts and larger of the ends
            if is_overlapping(interval, newInterval):
                # If merge, we don't append curr interval and instead "expand" newInterval to compare with next one
                # We expand until we cannot expand anymore (i.e., no longer overlaps with next interval in intervals)
                # If non-overlap, and newInterval comes before interval, and we haven't inserted it yet, then we should insert newInterval and then curr interval
                newInterval[0] = min(newInterval[0], interval[0])
                newInterval[1] = max(newInterval[1], interval[1])
            else:
                if newInterval[0] < interval[0]:
                    merged_intervals.append(newInterval)
                    newInterval = [float('inf'), float('inf')]
                merged_intervals.append(interval)

        # Case where we have not added newInterval into merged_intervals yet (no later interval that didn't overlap)
        if newInterval[0] != float('inf'):
            merged_intervals.append(newInterval)

        return merged_intervals
