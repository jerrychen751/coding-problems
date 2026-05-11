import heapq
from typing import List


class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        rooms_needed = 0
        intervals.sort() # This maintains the invariant that when processing a meeting, all meetings that started earlier can be checked to see whether any free spots have opened up
        min_heap = [] # stores (end, start) for a meeting room
        # Number of items in min_heap is number of meeting rooms used concurrently

        for interval in intervals:
            # Initial heap entry
            if len(min_heap) == 0:
                heapq.heappush(min_heap, (interval[1], interval[0]))
                rooms_needed = max(rooms_needed, 1)
                continue

            # For later intervals, there are two possibilities
            # The first is that interval[0] >= min_heap[0][0]
            # Then we use the same meeting room represented by min_heap[0] for new conference
            # and pop all meeting rooms with end time <= interval[0], then push (interval[1], interval[0]) in
            # Otherwise, the start time of this new meeting is earlier than any other meeting room's end time
            # so we need to open up a new room
            s, e = interval
            if s >= min_heap[0][0]:
                # Pop all meeting rooms with end time <= s
                while len(min_heap) > 0 and min_heap[0][0] <= s:
                    heapq.heappop(min_heap)

            heapq.heappush(min_heap, (e, s))
            rooms_needed = max(rooms_needed, len(min_heap))

        return rooms_needed
