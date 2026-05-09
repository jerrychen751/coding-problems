from typing import List


class Solution:
    def rotateTheBox(self, boxGrid: List[List[str]]) -> List[List[str]]:
        # Rotate 90 degrees right, so rightmost elements land on bottom
        # Form new rotated matrix of n x m
        # Simulate falling by iterating through elements right to left
        # Maintain a "ground" level indicating which row in rotated box is solid
        # If an element is a stone, it will fall to ground and ground decrements (smaller idx is higher)
        # If it is a stationary obstable, ground becomes curr idx
        # If it's air, we do nothing and continue iterating

        m = len(boxGrid)
        n = len(boxGrid[0])

        res = [['.' for _ in range(m)] for _ in range(n)]
        for i in range(m):
            ground = n - 1 # next valid idx location for element
            new_j = m - 1 - i
            for j in range(n - 1, -1, -1):
                x = boxGrid[i][j]
                new_i = j

                if x == '#':
                    # stone: fall to ground, ground increases in height
                    res[ground][new_j] = x
                    ground -= 1
                elif x == '*':
                    # obstacle: doesn't fall, stays at (new_i, new_j), ground rises to new_i in height
                    res[new_i][new_j] = x
                    ground = new_i - 1
                else:
                    # empty: move to (new_i, new_j), ground doesn't change
                    res[new_i][new_j] = x

        return res
