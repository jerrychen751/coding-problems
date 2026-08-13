from collections import deque
from typing import List

class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        # Monotonically decreasing queue
        # Monotonic in that queue stores elements in index order, maintaining decreasing order
        # For a new element, if smaller than last element in queue, append
        # Otherwise keep popping top of queue until either queue is empty or element at end of queue is larger than new element in sliding window

        # We rely on this "greedy" property where if we have a larger element later on in the queue
        # We can pop all smaller elements that appear earlier, since as long as those element can possibly be the max,
        # the larger curr element will always dominate and be considered instead, so we can delete smaller earlier-seen elements
        # Next, we maintain this queue of candidates and whenever left boundary of window increments,
        # We remove first element of queue if it is now excluded
        # With our invariant, there are 2 possibilities: element at front of queue is either a later element that's largest
        # or the next-best candidate if curr was excluded

        queue = deque()
        for i in range(k):
            # Initialize monotonic queue initially
            # Stores idx
            # Invariant is that idx is increasing, nums[idx] is decreasing
            num = nums[i]
            while queue and nums[queue[-1]] < num:
                queue.pop()
            queue.append(i)

        res = []
        left, right = 0, k - 1 # inclusive bounds of sliding window
        while right < len(nums):
            # At the beginning, check stack to update max element in curr window
            res.append(nums[queue[0]])

            # Next, process a shift in the window
            # nums[left] is gone, nums[right] is added (if in bounds)
            left += 1
            if queue[0] < left:
                queue.popleft()
            right += 1
            if right < len(nums):
                while queue and nums[queue[-1]] < nums[right]:
                    queue.pop()
                queue.append(right)

        return res
