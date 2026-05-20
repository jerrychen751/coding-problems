from collections import deque
from typing import List

class Solution:
    def minimumDeletions(self, nums: List[int]) -> int:
        # no matter what we need to start popping from either front or back
        # pick out the element closer to either edge (i.e. for both min and max element compute their dists to start and end of array)
        # simulate removal of that closer element from the closer dir
        # the other element is now that many removals closer to that dir
        # repeat for that element

        # To make this generalizable for k items, use a deque to track the closest elements to the ends
        # Use variables to track the beginning/end indices of the array (inclusive)
        # At each step, take deque(idx, element) and pop the one closest to either end
        # i.e., compare deque[0][0] and deque[-1][0] dist to beginning/end respectively
        # pop that element, adjust beg/end, find the next closest

        deletions = 0
        queue = deque([])
        beg, end = 0, len(nums) - 1
        min_idx, max_idx = 0, 0
        for i, num in enumerate(nums):
            if nums[i] < nums[min_idx]:
                min_idx = i
            elif nums[i] > nums[max_idx]:
                max_idx = i

        queue.append((min(min_idx, max_idx), nums[min(min_idx, max_idx)]))
        queue.append((max(min_idx, max_idx), nums[max(min_idx, max_idx)]))

        while len(queue) > 0:
            front = queue[0]
            back = queue[-1]
            d_front = front[0] - beg + 1 # deletions from front required
            d_back = end - back[0] + 1

            if d_front <= d_back:
                idx, e = queue.popleft()
                deletions += d_front
                beg = idx + 1
            else:
                idx, e = queue.pop()
                deletions += d_back
                end = idx - 1

        return deletions
