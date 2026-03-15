from typing import List
from collections import deque

class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        # Standard BFS (no need for set if state is updated on discovery)

        fresh_ct = 0
        queue = deque()
        m = len(grid)
        n = len(grid[0])
        time = 0

        for i in range(m):
            for j in range(n):
                if grid[i][j] == 2:
                    queue.append((i, j))
                elif grid[i][j] == 1:
                    fresh_ct += 1
        
        # Use fresh_ct to determine when to end processing of rotten oranges
        # Edge case: No fresh oranges to begin with
        if fresh_ct == 0:
            return 0

        def in_bounds(i: int, j: int, m: int, n: int) -> bool:
            return i >= 0 and i < m and j >= 0 and j < n
        
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        while queue and fresh_ct > 0:            
            # Perform BFS to infect neighboring oranges
            for _ in range(len(queue)):
                i, j = queue.popleft()
                for dir in dirs:
                    ni, nj = i + dir[0], j + dir[1]
                    if in_bounds(ni, nj, m, n) and grid[ni][nj] == 1:
                        grid[ni][nj] = 2 # make it rotten on discovery, so future cells don't duplicate it
                        fresh_ct -= 1
                        queue.append((ni, nj))
            
            time += 1
        
        if fresh_ct > 0:
            return -1
        
        return time

        '''
        # If all fresh oranges have no rotten orange adjacent to it, return -1
        # When one orange has infected another, it is effectively useless and we no longer need to track its location
        
        # Use a set to store infected oranges
        # Process all of them to get new infected oranges, which are added to another set
        # Process elements sequentially
        # O(n^2) time and O(n^2) space

        # Consider what state must be stored
        # Longest time for any orange to get infected thus far
        # Locations of oranges which currently infected

        # Approach
        # Track time with a variable, locations with a set, locations of newly infected oranges with another set
        # While curr infected oranges is a nonempty set
            # Infect adjacent cells; if there's an orange add it to new infected set
            # Remove orange from grid (change it to 0) because it can no longer do anything
            # If new set is nonempty, make that the curr set and make the new set empty again
            # Otherwise, we're done
        
            # In this process, track the time
        
        # return time

        curr_infected = set()
        new_infected = set()
        m = len(grid)
        n = len(grid[0])
        res = 0

        dirs = [
            (-1, 0), (1, 0),
            (0, 1), (0, -1)
        ]

        def in_bounds(m: int, n: int, i: int, j: int) -> bool:
            return i >= 0 and i < m and j >= 0 and j < n

        # First get initial state
        # Also check if all oranges do not have rotten neighbor

        fresh_ct = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 2:
                    grid[i][j] = 0
                    curr_infected.add((i, j))
                elif grid[i][j] == 1:
                    fresh_ct += 1
        
        if fresh_ct == 0:
            return 0
        
        # Next, we iterate until there are no more newly infected oranges
        while curr_infected or new_infected:
            while curr_infected:
                # Remove this orange from grid because it no longer does anything
                i, j = curr_infected.pop()

                # Infect adjacent cells
                for dir in dirs:
                    ni, nj =  i + dir[0], j + dir[1]
                    if in_bounds(m, n, ni, nj) and grid[ni][nj] == 1:
                        grid[ni][nj] = 0
                        new_infected.add((ni, nj))
                
            # Prepare for the next time tick
            if new_infected:
                res += 1
                curr_infected = new_infected
                new_infected = set()

        # Perform a final check for if there are any oranges remaining
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    return -1
        
        return res
        '''