from typing import List


class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        '''
        Bitwise modular arithmetic
        First count number of bits
        Then bits = [0] * nbits # bits[i] stores count of i-th bit -> mod it by 3 at the end to find identity of single num
        for i in range(nbits):
            for num in nums:
                bits[i] += num & (1 << i)

        res = 0
        for i in range(nbits):
            if bits[i] == 1:
                res += (1 << i)

        return res
        '''
        largest = max(abs(num) for num in nums)
        nbits = largest.bit_length() + 1

        bits = [0] * nbits
        for i in range(nbits):
            for num in nums:
                bits[i] += (num >> i) & 1

            bits[i] %= 3

        res = 0
        for i in range(nbits):
            if bits[i] == 1:
                res |= (1 << i) # uses unsigned int convention when building res

        if res & (1 << (nbits - 1)):
            # if we treated 1 << (nbits - 1) as positive, we need to undo it, so we subtract 2 * (1 << (nbits - 1))
            # which is subtracting 1 << nbits
            res -= (1 << nbits)

        return res
