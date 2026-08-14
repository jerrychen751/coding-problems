from typing import List


class Solution:
    def trap(self, height: List[int]) -> int:
        # Array of heights, representing elevation map
        # 2D, each height is a solid bar of height[i]
        # Determine amount of water trapped after raining

        # water doesn't accumulate on edges; treat boundaries as zeros
        # for each idx, for water to be trapped there, there needs to be a higher boundary somewhere to its left and right
        # limited by shorter of the two "effective heights", curr idx height can't be higher than shorter of the effective heights
        # effective height on left side of idx is max(height[:idx])
        # effective height on right side of idx is max(height[idx + 1:])

        n = len(height)
        left_effective = [0] * n
        right_effective = [0] * n
        max_from_left = height[0] # tracks max(height[:i]), excluding i
        for i in range(1, n):
            left_effective[i] = max_from_left
            max_from_left = max(max_from_left, height[i]) # take into consideration for next iteration
        
        max_from_right = height[-1]
        for i in range(n - 2, -1, -1):
            right_effective[i] = max_from_right
            max_from_right = max(max_from_right, height[i])
        

        total_water = 0
        for i in range(n):
            constraint = min(left_effective[i], right_effective[i])
            if height[i] < constraint:
                total_water += constraint - height[i]
        
        return total_water
