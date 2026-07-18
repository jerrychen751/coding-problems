from collections import deque, defaultdict
from typing import List


class Solution:
    def numOfMinutes(self, n: int, headID: int, manager: List[int], informTime: List[int]) -> int:
        # Each employee has exactly 1 manager (who is also an employee), except for head of company
        # which is at index headID with manager[headID] = -1
        
        # In a tree structure
        # The i-th employee takes informTime[i] to inform all of their reports
        # Return number of time to inform all employees
        
        # This is a directed graph; in order to determine time, we need to be able to travle from a manager
        # and iterate through each employee, at each level adding on the employee taking the longest time
        # Have a map mapping a manager to their employees
        # Then, start time at informTime[headID]
        # Level-order traversal -> maintain a queue of all people at a level
        # Keep a tracker for num_minutes
        # At any level of a queue, add all of their reports to the queue
        # Then for that level, add the max(informTime[i] for i in managers of that queue)
        
        managers = defaultdict(list)
        for i, m in enumerate(manager):
            if m != -1:
                managers[m].append(i)
        
        queue = deque([(headID, 0)])
        res = 0
        while len(queue) > 0:
            for _ in range(len(queue)):
                # Process per "level" of management tree
                curr, prev_time = queue.popleft()
                res = max(res, prev_time + informTime[curr])
                
                # Add reports for next level if any
                for report in managers[curr]:
                    queue.append((report, prev_time + informTime[curr]))
                    
        return res
