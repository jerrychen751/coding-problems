from typing import List
import random

class Solution:
    def minOperations(self, grid: List[List[int]], x: int) -> int:
        # m x n size grid
        # can only add +/- x to each value in grid
        # return least number of operations to make grid same value throughout

        # what makes it impossible to make it uni-valued?
        # if the difference between a single element and any other element on the board is not a multiple of x
        # then it's impossible
        # only have to pick out all pairs fixing a single element because if the difference between that element and all other
        # E.g., let the fixed element be a, and other elements be b, c, ...
        # if b-a = k1 * x and c-a = k2 * x...
        # then b-c = (k1 - k2) * x which is still a multiple of x

        # next, how do we return minimum number of operations to make grid uniform value?
        # try obtaining average across grid and then moving each element in the direction of the average
        # for any arbitrary element, start adding mulitples of x to move in the direction of the average
        # if we arrive, that's optimal and all other elements can arrive at average
        # if not, then there will be one below and one above (e.g., grid[0][0] + k1 * x < mean(grid), grid[0][0] + k2 * x > mean(grid)) and we just pick the closer one (if symmetric just pick either one)

        # fix: pick median and not mean

        # def kth_select(arr: list[int], k: int, lo: int, hi: int) -> int:
        #     """Find the k-th smallest element (0-indexed) within an array in O(n) time."""
        #     # Pick a random pivot
        #     # hoare-style partitioning w/ left right pointers
        #     # move pivot back; if pivot index is k we're done otherwise move onto left/right partition
        #     pivot_idx = random.randint(lo, hi)
        #     pivot = arr[pivot_idx]

        #     arr[lo], arr[pivot_idx] = arr[pivot_idx], arr[lo]
        #     i = lo + 1
        #     j = hi
        #     while True:
        #         while i <= j and arr[i] <= pivot:
        #             i += 1
        #         while i <= j and arr[j] >= pivot:
        #             j -= 1
        #         if i > j:
        #             break
        #         arr[i], arr[j] = arr[j], arr[i]
        #         i += 1
        #         j -= 1

        #     arr[lo], arr[j] = arr[j], arr[lo]

        #     if j < k: # current pivot idx is less than target; recurse into right partition
        #         return kth_select(arr, k, j + 1, hi)
        #     elif j == k:
        #         return pivot
        #     else:
        #         return kth_select(arr, k, lo, j - 1)

        m = len(grid)
        n = len(grid[0])
        reference = grid[0][0]

        nums = []
        for i in range(m):
            for j in range(n):
                # Check for whether it's possible
                if (grid[i][j] - reference) % x != 0:
                    return -1

                nums.append(grid[i][j])

        # median = kth_select(nums, len(nums) // 2, 0, m * n - 1)
        nums.sort()
        median = nums[len(nums) // 2]

        # sum(|x_i - t}) is minimized when t is the median
        # Here, if the length is odd, then the median is a single value fulfilling this minimization
        # If the length is even, the mathematical median is the average of two t1, t2.
        # However, all throughout [t1, t2] the sum of absolute error is minimized
        # Thus, we can pick t1/t regardless of even/odd cases

        res = 0
        for i in range(m):
            for j in range(n):
                num = grid[i][j]
                if num == median:
                    continue

                multiple = abs(num - median) // x
                res += multiple

        return res
