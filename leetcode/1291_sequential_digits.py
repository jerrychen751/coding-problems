from typing import List


class Solution:
    def sequentialDigits(self, low: int, high: int) -> List[int]:
        '''
        [low, high] is range for sequential digit generation
        will have at most 9 digits, no leading zeros
        identity of a generated sequential digit integer is determined only by start number and length
        start with first number; length ranges from len(low_s) to
        '''

        res = []
        digits = "123456789"

        for length in range(len(str(low)), len(str(high)) + 1):
            for start in range(10 - length):
                num = int(digits[start:start + length])
                if low <= num <= high:
                    res.append(num)
        return res
