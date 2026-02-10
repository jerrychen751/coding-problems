from typing import List

class Solution:
    def maxConsecutive(self, bottom: int, top: int, special: List[int]) -> int:
        # Given range of floors, from bottom to top (inclusive)
        # special contains floors which are denoted as special

        # We want to return the max number of conscutive floors without a special floor

        # Questions
        # Potential invalid inputs? Bottom/top being negative or top <= bottom?
        # What to do if bottom == top == special?

        # Simple solution
        # Sort special, append bottom and top to beginning / end
        # Take max(special[1:] - special[:-1])

        if len(special) == 0:
            return top - bottom

        special.sort()
        
        # Consider the difference between lowest special floor and bottom
        best = special[0] - bottom
        for i in range(1, len(special)):
            best = max(best, special[i] - special[i - 1] - 1) # this is exclusive, since both boundaries are special

        # Now consider the space between the top floor and the highest special floor
        best = max(best, top - special[-1])

        return best