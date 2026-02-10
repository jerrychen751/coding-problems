from typing import List

class Solution:
    def maxArea(self, height: List[int]) -> int:
        # Array of heights, where height[i] represents height of i-th vertical line
        # On a 2D coordinate plane, line extends from (i, 0) and (i, height[i])

        # Return the max amt of water the container can store overall

        # Assume height is non-negative? yes
        # Length of height indicates width of container? Like if the container is 10 wide, len(height)=10? yes
        # When computing area of water, we assume walls are thin? I.e., (0, 1) and (1, 1) stores 1x1=1 amt of water?

        # Approach
        # We basically want to maximize both the width and the min(h1, h2) of two walls
        # We can use two pointers at either end of the heights array, that way we have both width and heights
        # At each step, area = (j - 1) * min(height[i], height[j])
        # Then we need to close the wall somehow. Since we're moving inward, we want to keep the highest edge possible and then change the wall that's the "limiting factor" (only possible way to achieve higher water amt is if later we come across an even-higher container wall)
        # If they are the same height, then moving either wall inward should result in a symmetric result

        max_water = 0
        i = 0
        j = len(height) - 1
        while i < j:
            width = j - i
            min_height = 0
            if height[i] <= height[j]:
                min_height = height[i]
                i += 1
            else:
                min_height = height[j]
                j -= 1

            max_water = max(max_water, width * min_height)
        
        return max_water