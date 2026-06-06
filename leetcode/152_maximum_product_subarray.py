from typing import List


class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        # Return largest product that can be formed by multiplying elements of some subarray
        # Due to multiplication, as long as all values are nonzero and there are an even number of negatives
        # we should always multiply the entire array together

        # If there are an odd number of negatives and no zeros, divide by the largest negative number
        # (smallest by abs value)

        # If there are zeros, then split the array and recurse onto the two sides of the zero after performing max(0, prod)

        def max_prod_no_zeros(start: int, end: int) -> int:
            """Returns max prod possible for arr[start:end + 1] given the array has no zeros."""
            if start > end:
                return 0 # end was shrunk due to presence of 0
            if start == end:
                return nums[start]

            n_negative = 0
            largest_negative = float('-inf')
            largest_negative_idx = 0
            prod = 1
            for i in range(start, end + 1):
                num = nums[i]
                if num < 0:
                    n_negative += 1
                    if num > largest_negative:
                        largest_negative = num
                        largest_negative_idx = i
                prod *= num

            if n_negative & 1 == 0:
                return prod

            # How to find max possible product of an array given it has an odd number of negatives
            # A singular negative can be excluded and we're guaranteed positive
            # If we only consider negative numbers, we CANNOT exclude any negative in the center due to subarray requirements
            # Since including more negative numbers is guaranteed to raise the product
            left_prod = 1 # track leftmost and rightmost products up until first negative
            right_prod = 1
            for i in range(start, end + 1):
                left_prod *= nums[i]
                if left_prod < 0:
                    break

            for i in range(end, start - 1, -1):
                right_prod *= nums[i]
                if right_prod < 0:
                    break

            return prod // max(left_prod, right_prod) # divide by larger of the two (less negative)

        max_prod = nums[0]
        curr_start, curr_end = 0, 0
        for i in range(len(nums)):
            num = nums[i]
            if num == 0:
                curr_end = i - 1
                max_prod = max(max_prod, max_prod_no_zeros(curr_start, curr_end), 0)
                curr_start = i + 1
                curr_end = i + 1
            else:
                curr_end += 1

        max_prod = max(max_prod, max_prod_no_zeros(curr_start, curr_end - 1))
        return max_prod
