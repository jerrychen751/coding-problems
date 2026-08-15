from typing import List


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        """
        1, 2, 3
        nums is unsorted
        not looking for a subarray of nums with consecutive integers
        but rather subset which is consecutive

        check if new val is adjacent to borders of any group
        2 maps; start->end, end->start
        for some num, check if num + 1 in starts or ends

        longest = 0
        start_end = {} # see if new num expands interval on left end
        end_start = {} # see if new num expands interval on right end
        for num in nums:
            if num is not adjacent to any sequence seen so far; num + 1 not in start_end and num - 1 not in end_start
                becomes its own component; added to start_end and end_start

            if num is an earlier start; num + 1 in start_end
                update start_end and its corresponding end_start
                update longest with max(longest, end - start + 1)
            if num is a later end; num - 1 in end_start
                update start_end and end_start
                update longest

        return longest
        """

        longest = 0
        start_end = {}
        end_start = {}
        seen = set()
        for num in nums:
            if num in seen:
                continue

            # Handle case where num + 1 in start_end AND num - 1 in end_start -> the two components need to be joined again
            if num + 1 in start_end and num - 1 in end_start:
                # end_start[num] <= num <= start_end[num]
                # start_end[earliest] needs to be updated from num to latest
                # end_start[latest] needs to be updated from num to earliest
                # things that start/end with num need to go b/c it's in the middle already
                earliest = end_start[num - 1]
                latest = start_end[num + 1]
                start_end[earliest] = latest
                end_start[latest] = earliest
                del start_end[num + 1]
                del end_start[num - 1]
                longest = max(longest, latest - earliest + 1)
            elif num + 1 in start_end: # num is earlier start
                end = start_end[num + 1]
                del start_end[num + 1]
                start_end[num] = end
                end_start[end] = num
                longest = max(longest, end - num + 1)
            elif num - 1 in end_start: # num is new later end
                start = end_start[num - 1]
                del end_start[num - 1]
                start_end[start] = num
                end_start[num] = start
                longest = max(longest, num - start + 1)
            else:
                start_end[num] = num
                end_start[num] = num
                longest = max(longest, 1)

            seen.add(num)

        return longest
