from collections import defaultdict
from typing import List

class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        """
        k is target, number of subarrays whose sum is k
        subarray is distinct by indices
        array is not sorted

        Iterate through all possible subarrays, sum, O(n^2)

        Prefix sum?
        Sorting?
        Is there a way to know after reaching target whether subarray needs to keep expanding

        [1, 2, 3, -3, 3]
        repeat values in prefix sum?
        store number of ways to achieve a certain sum

        {0: 1, 3: 2} - sum mapped to number of ways to achieve that sum via subarray
        from nums[i + 1:??] where ?? can end anywhere between i + 1..end

        As we iterate through array, from right to left, we have idx i
        cache mapping some subarray from nums[i+1:??] and all possible values
        O(n) space at most
        Each time, we need to update whole cache

        {}
        {3: 1}
        {-3: 1, 0: 1} -> 1 new entry, all other entries are shifted by a fixed amount (being nums[i + 1])

        Any subarray can be represented as diff of prefix sums
        Suppose we're at nums[i]; goal is for nums[i] + ? == k, where ? may be empty subarray
        or some non-empty subarray which is of value ? = suffix_sum[i + 1] - suffix_sum[j].

        Basically, we're guaranteed that for it to be a subarray, we have suffix sum from i + 1 onward, and we're just looking for some count of suffixes forming difference between suffix_sum[i + 1] - (k - nums[i])

        nums[i] + x = k
        x = suffix_sum - some other suffix sum seen in suffix_sum_ct
        x = k - nums[i] = suffix_sum - a
        a = suffix_sum + nums[i] - k
        """
        suffix_sum_ct = defaultdict(int)
        suffix_sum_ct[0] = 1
        suffix_sum = 0
        n = len(nums)
        res = 0
        for i in range(n - 1, -1, -1):
            num = nums[i]
            target = suffix_sum + num - k
            res += suffix_sum_ct[target]

            suffix_sum += num
            suffix_sum_ct[suffix_sum] += 1

        return res
