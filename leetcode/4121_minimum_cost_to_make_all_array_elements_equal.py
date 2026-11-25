class Solution:
    def minCost(self, nums: list[int]) -> int:
        '''
        Index chosen cannot be first/last
        Iterate through, pick an index, if diff from prev then cost is (n - 1) * nums[i]
        If same from prev then it's prev_idx * nums[i] + (n - i - 1) * nums[i]
        '''
        res = float('inf')
        prev = nums[0]
        prev_idx = 0
        n = len(nums)
        for i in range(1, n):
            num = nums[i]
            if num == prev:
                res = min(res, prev_idx * prev + (n - i - 1) * num)
            else:
                if i == n - 1: continue
                res = min(res, (n - 1) * num)
                prev = num
                prev_idx = i

        return res
