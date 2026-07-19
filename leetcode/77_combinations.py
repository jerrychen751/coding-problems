from typing import List


class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        # n total numbers from 1..n
        # return all combinations of k numbers possible

        combinations = []
        def backtrack(start: int, curr_nums: list[int]) -> None:
            if len(curr_nums) == k:
                combinations.append(curr_nums.copy())
                return

            for i in range(start, n + 1):
                curr_nums.append(i)
                backtrack(i + 1, curr_nums)
                curr_nums.pop()

        backtrack(1, [])
        return combinations
