class Solution:
    def minimumSteps(self, s: str) -> int:
        '''
        00101
        min steps when 0 only ever moves left, 1 only ever moves right
        i, j pointers
        Invariant: i points to location of leftmost 1 if i != j otherwise s[i] == s[j] == '0'
        '''
        n = len(s)
        i, j = 0, 0
        swaps = 0
        while j < n:
            if s[j] == '0':
                swaps += (j - i)
                j += 1
                i += 1
            else:
                j += 1

        return swaps
