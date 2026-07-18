from collections import deque
from typing import List

class Solution:
    def longestSubarray(self, nums: List[int], limit: int) -> int:
        # Maintain window
        # Track 2 info within window: min and max
        # Iterate from j=0..n-1 (end of window)
        # Start of window is initially i=0
        # As we iterate through, if abs(max - min) > limit, then start moves to the rightmost index containing an element still violating abs(max - nums[rightmost_idx]) + 1
        
        # Monotonic queues -> indices in queues are strictly increasing and values
        # for min_queue are non-decreasing and values for max_queue are non-increasing
        
        # For min queue, we add a new value by popping all larger values (comp to new value) and then adding new value
        # That's because those larger values were seen earlier (left of new value) so there's no window where
        # those seen values become min in window (either they're excluded in new window or new window contains both)
        
        # Same logic for max queue
        
        # Maintain both these queues when we see a new value in nums
        # Determine if abs(nums[max_queue[0]] - nums[min_queue[0]]) > limit
        # If so move left
        # And then remove elements from front of queue which are no longer in window
        
        min_q = deque()
        max_q = deque()
        i = 0
        res = 0
        for j in range(len(nums)):
            # Update queues with new seen value
            while min_q and nums[min_q[-1]] > nums[j]:
                min_q.pop()
            min_q.append(j)
            while max_q and nums[max_q[-1]] < nums[j]:
                max_q.pop()
            max_q.append(j)
            
            # Determine if curr window violates limit
            while nums[max_q[0]] - nums[min_q[0]] > limit:
                i += 1
                
                while min_q and min_q[0] < i:
                    min_q.popleft()
                while max_q and max_q[0] < i:
                    max_q.popleft()
            
            res = max(res, j - i + 1)
        
        return res
