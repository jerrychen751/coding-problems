from typing import List

class BruteForce:
    def maximumSumOfHeights(self, heights: List[int]) -> int:
        # Goal: form mountain-shaped towers, where tower heights are non-decreasing, reaching a maximum, and then non-increasing
        # Return maximum possible sum of heights, or essentially remove as few bricks as possible
        max_height_sum = 0
        total_height_sum = sum(heights)

        for peak_idx in range(len(heights)):
            # ensure heights[:peak] is non-decreasing
            # ensure heights[peak:] is non-increasing
            # sum over as we iterate
            bricks_removed = self._removeBricks(heights, peak_idx)
            max_height_sum = max(max_height_sum, total_height_sum - bricks_removed)

        return max_height_sum
    
    def _removeBricks(self, heights: List[int], peak_idx: int) -> int:
        heights = heights.copy()
        # return the number of bricks removed
        # ensure left is non-increasing
        bricks_removed = 0
        for i in range(peak_idx, -1, -1):
            if i == 0:
                continue

            diff = heights[i] - heights[i - 1]
            if diff < 0:
                heights[i - 1] -= abs(diff)
                bricks_removed += abs(diff)

        for j in range(peak_idx, len(heights) - 1):
            diff = heights[j + 1] - heights[j]
            if diff > 0:
                heights[j + 1] -= diff
                bricks_removed += diff
        
        return bricks_removed

class DynamicProgramming:
    def maximumSumOfHeights(self, heights: List[int]) -> int:
        # Attempt to cut repeated work of recalculating left/right partitions after a new peak
        # Only recalculate the portions that were previously flattened -> this means tracking the original potentials/heights for those indices
        # Note that sum_at_peak_i = dp_left[i] + dp_right[i] - heights[i] (inclusion-exclusion)

        n = len(heights)
        dp_left = [0] * n # dp_left[i] is the max sum of non-decreasing subarray ending at i; dp_left[i] = heights[i] * (i - j) + dp_left[j], where j is nearest index to the left of i that is not greater than heights[i]
        dp_right = [0] * n # dp_right[i] is the max sum of non-increasing subarray ending at i; dp_right[i] = heights[i] * (j - i) + dp_right[j], where j is nearest index to the right of i that is not greater than heights[i]

        # Now the question becomes: how do we find j efficiently as we iterate through i
        stack = [] # stores j; monotonic in that if stack contains [i, j, k] then heights[i] < heights[j] < heights[k]
        for i in range(n):
            while stack and heights[stack[-1]] >= heights[i]:
                stack.pop()
            
            if stack:
                j = stack[-1]
                dp_left[i] = heights[i] * (i - j) + dp_left[j]
            else: # there is no tower that is shorther than heights[i] to the left of i
                dp_left[i] = heights[i] * (i + 1)
        
            stack.append(i)

        stack = []
        for i in range(n - 1, -1, -1):
            while stack and heights[stack[-1]] >= heights[i]:
                stack.pop()

            if stack:
                j = stack[-1]
                dp_right[i] = heights[i] * (j - i) + dp_right[j]
            else: # there is no tower that is shorter than heights[i] to the right of i
                dp_right[i] = heights[i] * (n - i)
            
            stack.append(i)

        max_height_sum = 0
        for i in range(n):
            sum_at_peak_i = dp_left[i] + dp_right[i] - heights[i]
            max_height_sum = max(max_height_sum, sum_at_peak_i)
        
        return max_height_sum

    
if __name__ == '__main__':
    s1 = DynamicProgramming()
    print(s1.maximumSumOfHeights([3,2,5,5,2,3]))
