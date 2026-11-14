import random
from bisect import bisect_left

class Solution:

    def __init__(self, w: list[int]):
        self.w = w
        self.prefix_sum = w.copy()
        for i in range(1, len(w)):
            self.prefix_sum[i] += self.prefix_sum[i - 1]

    def pickIndex(self) -> int:
        return bisect_left(self.prefix_sum, random.randint(1, self.prefix_sum[-1]))

    # [1, 3]
    # self.prefix_sum = [1, 4]
    # we want 1/4 chance to pick 0, 3/4 chance to pick 1
    # 0, 1, 2, 3

# Your Solution object will be instantiated and called as such:
# obj = Solution(w)
# param_1 = obj.pickIndex()
