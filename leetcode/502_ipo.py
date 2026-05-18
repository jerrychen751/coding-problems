import heapq
from typing import List

class Solution:
    def findMaximizedCapital(self, k: int, w: int, profits: List[int], capital: List[int]) -> int:
        # Want maximal profits; only need certain amount of capital before starting a project
        # Projects don't cost anything (assume that given starting capital, revenue - cost is already accounted for in profits)
        # At most k projects

        # Use a heap to find maximal profits, except that it's capped by w (current capital)
        # Don't want to keep popping off of heap each time to find first project within capital threshold

        # Have a ptr in capital
        # Only add profits[i] to heap when w >= capital[i]
        # First, sort to obtain a list of (profit, capital) in ascending order of capital
        # Maintain an index cap_idx pointing to the very first project that costlier than current w
        # While k > 0, add to max-heap by pushing profits[i] until projects[cap_idx][1] > w, increment cap_idx
        # Pop from max-heap to obtain best project to complete, increase w, decrease k
        # Repeat until k == 0 or no available project left in heap

        # O(nlogn) where nlogn includes sort step, + heap (we may push all n elements to heap and pop off k where n >= k)

        projects = sorted(list(zip(profits, capital)), key=lambda x:x[1])
        max_heap = [] # use -profit since python implementation is min-heap
        cap_idx = 0
        while k > 0:
            # Add to max-heap
            while cap_idx < len(projects) and projects[cap_idx][1] <= w:
                heapq.heappush(max_heap, -projects[cap_idx][0])
                cap_idx += 1

            # Pop, increase w, decrease k
            if len(max_heap) == 0:
                break

            w += (-heapq.heappop(max_heap))
            k -= 1

        return w
