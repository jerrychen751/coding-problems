from typing import List


class Solution:
    def numberOfWeeks(self, milestones: List[int]) -> int:
        # each week we can finish exactly 1 milestone of 1 project
        # cannot work on same project's milestones two consecutive weeks
        # return max number of weeks we can work on projects without violating one of these rules

        # best case scenario is sum(milestones)
        # One idea is to build a max-heap and then always subtract from 2 largest values at any time, and see how far that gets us until there's only 1 element in the heap remaining

        # The key insight is that only the largest in relation to everything else matters
        # That's the only blocking factor

        largest = 0
        remaining_sum = 0
        for num in milestones:
            if num > largest:
                remaining_sum += largest
                largest = num
            else:
                remaining_sum += num

        if largest <= remaining_sum + 1:
            return largest + remaining_sum

        return remaining_sum * 2 + 1
