from typing import List


class Solution:
    def shortestDistanceColor(self, colors: List[int], queries: List[List[int]]) -> List[int]:
        k = 3 # colors
        n = len(colors)
        dists = []
        for color in range(1, k + 1):
            dist = [float('inf')] * n
            # 2 passes; from left and from right
            # 1st pass from the left
            nearest = -1 # index of nearest element
            for i in range(n):
                if colors[i] == color:
                    dist[i] = 0
                    nearest = i
                else:
                    if nearest != -1:
                        dist[i] = i - nearest

            # 2nd pass from the right
            nearest = -1
            for i in range(n - 1, -1, -1):
                if colors[i] == color:
                    nearest = i
                else:
                    if nearest != -1:
                        dist[i] = min(dist[i], nearest - i)

            dists.append(dist)

        res = []
        for i, c in queries:
            if dists[c - 1][i] == float('inf'):
                res.append(-1)
            else:
                res.append(dists[c - 1][i])

        return res
