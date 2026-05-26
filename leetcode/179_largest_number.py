import heapq
from typing import List

class Number:
    def __init__(self, num: str) -> None:
        self.val = num

    def __lt__(self, other: Number) -> bool:
        # If same length, return larger val
        # If different lengths, only compare up to shorter length

        # Reverse this so that largest numbers are treated as smallest
        # So they would be at the top of min-heap
        if self.val + other.val > other.val + self.val:
            # self is "larger" so it's treated as smaller
            return True
        else:
            return False

class Solution:
    def largestNumber(self, nums: List[int]) -> str:
        max_heap = []
        # Default is min-heap
        largest_num = [] # list of strs, build by popping from max_heap, join at end
        for num in nums:
            heapq.heappush(max_heap, Number(str(num)))

        while len(max_heap) > 0:
            x = heapq.heappop(max_heap)
            largest_num.append(x.val)

        res = "".join(largest_num)
        return str(int(res))
