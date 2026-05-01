from typing import List


class Solution:
    def smallestSubarrays(self, nums: List[int]) -> List[int]:
        # We want smallest interval i...j so that bitwise OR of values within subarray is equal to max(B_ik)
        # So basically the shortest length that offers max over subarrays which start at i

        # Naive method is O(n^2), where we iterate through each index of nums, then iterate from i...end to find maximum bitwise OR
        # within minimum distance

        # Say that nums[i] was 010101
        # We basically want to know indices that contain 1's at bits 1, 3, 5

        # We want to find the shortest prefix from i...end which has the same bits as the full
        # With increasing length, it's monotonically increasing
        # Base case is the rightmost element; length is just 1
        # iterating left, we OR that with the newly introduced element and set that as the target/max possible bitwise OR
        # XOR new element with target to see which indices/bits we're missing
        # Maintain a table, where arr[i] = leftmost appearance of bit i being 1 in the elements we've seen so far as we're iterating leftward
        # Take the max of those values (idx); final length is max_bit_idx - i + 1

        def update_earliest(earliest: list[int], num: int, idx: int) -> None:
            i = 0
            while num > 0:
                if num & 1 == 1:
                    earliest[i] = idx
                num >>= 1
                i += 1

        n = len(nums)
        earliest = [-1] * 32 # leftmost bit occurrence table
        res = [0] * n

        target = 0
        for i in range(n - 1, -1, -1):
            target |= nums[i]
            missing_bits = target ^ nums[i]

            # Find max idx of nums which provides a missing bit
            max_idx = i
            bit_pos = 0
            while missing_bits > 0:
                if missing_bits & 1 == 1:
                    max_idx = max(max_idx, earliest[bit_pos])
                missing_bits >>= 1
                bit_pos += 1

            update_earliest(earliest, nums[i], i)
            res[i] = max_idx - i + 1

        return res
