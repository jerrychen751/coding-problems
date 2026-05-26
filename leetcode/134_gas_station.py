from typing import List

class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        # There is one unique gas station idx that we can start at
        # Travel in clockwise distance (circular route; increasing index numbers)
        # idx = (start + i) % n; i iterates from 0...n-1
        # if car can land on (idx - 1) % n then we can complete

        # we can compute a diff array of gas - cost -> starting point must be positive
        # if sum(diff) < 0, then we definitely can't make it across
        # find circular subarray where the remaining elements are only individually negative + sum(diff) >= 0 -> start of subarray is answer

        # sum diffs starting from a particular index; sum cannot go negative at any point

        # We can use the fact that there's only 1 correct starting index to our advantage
        # When we traverse diffs, we keep track of current tank
        # Take index 0 as candidate for start. If it's negative, then we can't even move off of it.
        # If it's zero/positive, we "stick with it" for now and keep moving forward. If at any point tank becomes negative, then we need to start over using next index. Between the next index and candidate starting index, candidate start is always better than the ones in between but it still didn't work so we skip all in between.

        curr_gas = 0
        start_idx = 0
        sum_diff = 0
        for i, d_gas in enumerate(gas):
            diff = d_gas - cost[i]
            sum_diff += diff
            curr_gas += diff
            if curr_gas < 0:
                start_idx = i + 1
                curr_gas = 0
                continue


        return start_idx if sum_diff >= 0 else -1
