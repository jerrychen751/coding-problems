from typing import List


class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        # Fix 1 -> becomes 3-sum
        # let n = len(nums)
        # iterate through 0...n-4; leave n-3, n-2, n-1 idx elements
        # this way we fix one element, obtaining a new target = target - nums[a]
        # then, we do the same for nums[a + 1:]
        # iterate through a+1...n-3; fix one element nums[b] and then use two pointers (c, d) at b + 1 and n - 1
        # for unique quadruplets, we sort the array nums first and then for a/b if the next element is same as previous then we skip this iteration

        if nums is None or len(nums) < 4:
            return []

        n = len(nums)
        nums.sort()

        def k_sum(start: int, k: int, target: int) -> list[list[int]]:
            # Return list of k-length lists which sum to target

            if n - start < k:
                return []

            # Pruning optimization
            # start is smallest element in remaining array
            # if start * k > target, picking elements from remaining options is definitely too large
            # if nums[-1] * k < target, picking elements from options is definitely too small
            if nums[start] * k > target or nums[-1] * k < target:
                return []

            # Base case; k == 2
            if k == 2:
                res = []
                i = start
                j = n - 1

                while i < j:
                    x1 = nums[i]
                    x2 = nums[j]
                    if x1 + x2 == target:
                        res.append([x1, x2])
                        i += 1
                        j -= 1
                        while i < j and nums[i] == nums[i - 1]:
                            i += 1
                        while i < j and nums[j] == nums[j + 1]:
                            j -= 1
                    elif x1 + x2 < target:
                        i += 1
                    else:
                        j -= 1

                return res

            # Otherwise, fix one digit and recurse
            # i goes up to n - k, so then there are k - 1 spaces left
            res = []
            for i in range(start, n - k + 1):
                # Skip duplicates
                # If nums[i] == nums[i - 1], then all results for nums[i] will already be covered by nums[i - 1]
                if i > start and nums[i] == nums[i - 1]:
                    continue

                for sub in k_sum(i + 1, k - 1, target - nums[i]):
                    res.append([nums[i]] + sub)

            return res

        return k_sum(0, 4, target)
