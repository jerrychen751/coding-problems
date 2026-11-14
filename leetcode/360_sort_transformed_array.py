from bisect import bisect_left

class Solution:
    def sortTransformedArray(self, nums: list[int], a: int, b: int, c: int) -> list[int]:
        '''
        All values may be positive or negative
        Return transformed array using formula in sorted order
        Original array nums is in sorted order
        '''
        # Edge case: not a parabola
        if a == 0:
            if b >= 0:
                return [b * x + c for x in nums]
            else:
                return [b * x + c for x in nums[::-1]]

        # Determine x-coordinate of vertex of parabola; use two pointers to explore left/right for increasing transformed values
        # For a > 0, the following works
        # For a < 0, we start at the maximum and should continue looking for maxes and reverse the list at the end
        x = -b / (2 * a)
        j = bisect_left(nums, x)
        i = j - 1

        # i explores left side of parabola, j explores right side of parabola
        n = len(nums)
        res = []
        while i >= 0 and j < n:
            i_val = a * nums[i] ** 2 + b * nums[i] + c
            j_val = a * nums[j] ** 2 + b * nums[j] + c
            # Depending on direction of parabola, we want to take different actions based on comparison results
            # For upward, we take smaller of values to construct result in order
            # For downward, we take larger of the two values and reverse at the end
            if i_val <= j_val:
                if a > 0:
                    res.append(i_val)
                    i -= 1
                else:
                    res.append(j_val)
                    j += 1
            else:
                if a > 0:
                    res.append(j_val)
                    j += 1
                else:
                    res.append(i_val)
                    i -= 1

        while i >= 0:
            i_val = a * nums[i] ** 2 + b * nums[i] + c
            res.append(i_val)
            i -= 1

        while j < n:
            j_val = a * nums[j] ** 2 + b * nums[j] + c
            res.append(j_val)
            j += 1

        return res if a > 0 else res[::-1]
