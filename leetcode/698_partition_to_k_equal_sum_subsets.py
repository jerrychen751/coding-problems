from typing import List


class Solution:
    def canPartitionKSubsets(self, nums: List[int], k: int) -> bool:
        # target for each subset == sum(nums) / k
        # if sum(nums) / k is not an integer, it's impossible so return false
        # if max(nums) > target it's also impossible

        # sort the array
        # for each subset, try adding elements until we achieve target, and then that subset is finalized
        # no, a greedy approach wouldn't work
        if sum(nums) % k != 0:
            return False
        target = sum(nums) // k

        nums.sort(reverse=True)
        buckets = [0] * k # accumulated sum across k groups
        def backtrack(i: int) -> bool:
            if i == len(nums):
                return True

            for j in range(k):
                if buckets[j] + nums[i] <= target:
                    buckets[j] += nums[i]

                    if backtrack(i + 1):
                        return True

                    # Backtracking step; if this path doesn't work undo it and try adding to next bucket
                    buckets[j] -= nums[i]
                    if buckets[j] == 0:
                        return False # given current state, there's no point in trying remaining buckets[j+1:]
                        # because explored paths are isomorphic
                        # if j is empty, it's guaranteed that buckets[j+1:] will also be empty
                        # and so there's no point in continuing down this state

            return False # none of the buckets work for adding -> false for this path

        return backtrack(0)
