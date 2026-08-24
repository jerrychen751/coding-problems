class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        '''
        Return triplets such that indices used are different and they sum to zero
        Sort numbers so that finding pairs summing to target is O(n) instead of O(n^2)
        sort(nums)
        for i in 0..n-3:
            target = 0 - nums[i]
            j = i + 1
            k = n - 1
            while j < k:
                check if nums[j] + nums[k] sum to target
                if so, we've found triplet
                if < target, increment j
                if > target, decrement k

        return triplets

        since j/k are in window to the right of i, there's no duplicate triplets
        '''
        s_nums = sorted(nums)
        n = len(nums)
        res = []
        for i in range(n - 2):
            if i > 0 and s_nums[i] == s_nums[i - 1]:
                continue
            target = 0 - s_nums[i]
            j = i + 1
            k = n - 1
            while j < k:
                pair_sum = s_nums[j] + s_nums[k]
                if pair_sum == target:
                    res.append([s_nums[i], s_nums[j], s_nums[k]])
                    j += 1
                    k -= 1
                    while j < k and s_nums[j] == s_nums[j - 1]:
                        j += 1
                    while j < k and s_nums[k] == s_nums[k + 1]:
                        k -= 1
                elif pair_sum < target:
                    j += 1
                else:
                    k -= 1
        return res
