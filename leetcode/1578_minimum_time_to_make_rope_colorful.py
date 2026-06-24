from typing import List


class Solution:
    def minCost(self, colors: str, neededTime: List[int]) -> int:
        # we can remove certain indices at a cost
        # want different colors, represented by chars, in sequence i.e. no adjacent same color / duplicate letters
        # we pay attention only to the substrings w/ duplicate letters; since we're removing nothing we do to non-problematic substrings will be beneficial

        # for a base case of len(substring) == 2, we pick the smaller of the two to remove
        # still for longer substrings, we only keep the max so we track running sum of substring time and just subtract the shortest, adding that to res which is a total time tracker

        total_time = 0
        curr_time = neededTime[0]
        max_time_in_substring = neededTime[0]
        n = len(colors)
        for i in range(1, n):
            t = neededTime[i]
            # if diff color, clear prev trackers
            if colors[i] != colors[i - 1]:
                # First add time needed to clear prev substring, if any
                total_time += (curr_time - max_time_in_substring)

                # Now reset
                curr_time = t
                max_time_in_substring = t
                continue

            # we have some substring of len >= 2
            curr_time += t
            max_time_in_substring = max(max_time_in_substring, t)

        # At the end the last segment might be substring of duplicate letters
        # so we add that time as well to total
        total_time += (curr_time - max_time_in_substring)
        return total_time
