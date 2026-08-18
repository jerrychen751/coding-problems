from typing import List


class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        '''
        cost is manhattan distance between two points
        could be a single point -> return 0
        n-1 edges
        0,0 1,0 0,1

        MST, Kruskal's Algorithm
        Union-Find
        n^2 -> min-heap -> use only cheapest edge which connects two different components
        n^2 log n

        Prim's Algorithm
        n^2 time, n space

        Let index in points represent the node
        Keep a used tracker for points already in MST

        start off with points[0]
        used[0] = True
        dists = [inf] * n # maintains shortest dist from points[i] to any node in component
        cost = 0
        repeat n - 1 times:
            keep next point tracker
            determine next point to add: not used, cheapest of all points seen so far

            update used for next point to add
            update cost
            using this new point, calculate dist to all non-used points and improve dists if it's better
        '''
        def get_dist(p1: list[int], p2: list[int]) -> int:
            return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

        n = len(points)
        if n == 0:
            return 0

        used = [False] * n
        dists = [float('inf')] * n
        dists[0] = 0
        cost = 0
        for _ in range(n):
            next_point = -1
            for i in range(n):
                if not used[i] and (next_point == -1 or dists[i] < dists[next_point]):
                    next_point = i

            used[next_point] = True
            cost += dists[next_point]
            point = points[next_point]
            for i in range(n):
                if not used[i]:
                    neighbor = points[i]
                    neighbor_dist = get_dist(point, neighbor)
                    if neighbor_dist < dists[i]:
                        dists[i] = neighbor_dist

        return cost
