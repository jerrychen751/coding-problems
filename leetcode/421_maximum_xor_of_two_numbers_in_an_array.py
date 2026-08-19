from typing import List


class Solution:
    def findMaximumXOR(self, nums: List[int]) -> int:
        '''
        at least 1 element
        non-negative

        iterate through all pairs -> track largest XOR
        o(n^2) time

        if a ^ b = c, then a ^ c = b
        [3, 10, 5, 25, 2, 8]
        00011 
        01010
        00101 <-
        11001 <-
        00010
        01000

        greedy approach starting from leftmost bit
        construct value of max XOR
        11111
        look one bit at a time starting from the beginning of the bitwise xor
        xor = nums[i] ^ nums[j] for some i,j in nums (may be the same number but shouldn't)
        look at just leftmost bit; can we form 1xxxx
        YES, 25 and any other number
        can we form 11xxx
        YES, 25 and 3/5/2 work
        can we form 111xx
        YES, 25 and 3 work
        we end here
        '''
        nbits = max(nums).bit_length()
        max_xor = 0 # keep track of the maximum xor that can be formed
        for i in range(nbits - 1, -1, -1):
            max_xor <<= 1 # free the next bit (i-th bit from left starts out as 0)
            curr_xor = max_xor | 1 # start out by setting 1 in rightmost bit of max_xor; check if this can be achieved with our prefixes
            prefixes = {num >> i for num in nums}
            possible = any(curr_xor ^ p in prefixes for p in prefixes)
            if possible:
                max_xor |= 1
            
        
        return max_xor
