class Solution:
    def rangeBitwiseAnd(self, left: int, right: int) -> int:
        '''
        [left, right]
        no negatives
        
        left = 5 = 0101
        mid = 6 = 0110
        right = 7 = 0111
        '''
        shifts = 0
        while left != right:
            left >>= 1
            right >>= 1
            shifts += 1
        
        return left << shifts
