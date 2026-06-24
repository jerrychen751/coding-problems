from typing import List


class Solution:
    def maxScoreIndices(self, nums: List[int]) -> List[int]:
        # left = nums[0..i-1]
        # right = nums[i..n-1] -> includes pivot
        # partition can be empty
        # find highest possible division score: # of 0's in left + # of 1's in right
        # return list of pivot indices allowing for highest division score

        best_score = 0
        res = [] # replace each time best_score increases
        total = sum(nums)
        running_total = 0 # at a pivot i the value (i - running_total) where running_total is sum(nums[:i]) is number of zeros
        # combine this with (total - running_total) and we get sum(nums[i:]) which is number of 1's on right side
        n = len(nums)
        for i in range(n + 1):
            left_score = i - running_total
            right_score = total - running_total

            curr = left_score + right_score
            if curr > best_score:
                best_score = curr
                res = [i]
            elif curr == best_score:
                res.append(i)

            # afterward update totals
            if i < n:
                running_total += nums[i]

        return res
