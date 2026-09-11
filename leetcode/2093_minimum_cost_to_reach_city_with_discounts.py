import heapq
from collections import defaultdict
from typing import List

class Solution:
    def minimumCost(self, n: int, highways: List[List[int]], discounts: int) -> int:
        '''
        n cities, 0..n-1
        undirected edges of [u, v, cost]
        discounts is number of times we can halve cost
        used once per edge
        return min cost to go from city 0 to n-1, or -1 if not possible

        dijkstra's algorithm for shortest path, but we also track discounts used
        dists mapping (node, discounts_remaining) -> dist from 0 to node
        min_heap stores (dist, node, discounts_remaining)
        seen set storing (node, discounts_remaining)

        (node, discounts_remaining) is sufficient state because we can compute all future path costs from it
        dists, seen can both become arrays
        '''
        dists = [[float('inf') for _ in range(discounts + 1)] for _ in range(n)]
        seen = [[False for _ in range(discounts + 1)] for _ in range(n)]
        dists[0][discounts] = 0
        min_heap = [(0, 0, discounts)]

        graph = defaultdict(list)
        for u, v, c in highways:
            graph[u].append((v, c))
            graph[v].append((u, c))

        while min_heap:
            d, u, discounts_remaining = heapq.heappop(min_heap)
            if u == n - 1:
                return d

            if seen[u][discounts_remaining]:
                continue
            seen[u][discounts_remaining] = True

            # no discount used
            for v, c in graph[u]:
                new_cost = d + c
                if new_cost < dists[v][discounts_remaining]:
                    dists[v][discounts_remaining] = new_cost
                    heapq.heappush(min_heap, (new_cost, v, discounts_remaining))

                if discounts_remaining > 0:
                    new_discounts = discounts_remaining - 1
                    discounted_cost = d + c // 2
                    if discounted_cost < dists[v][new_discounts]:
                        dists[v][new_discounts] = discounted_cost
                        heapq.heappush(min_heap, (discounted_cost, v, new_discounts))

        return -1
