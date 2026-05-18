class Solution:
    def maximumXor(self, s: str, t: str) -> str:
        # s is unchanged, rearrange characters of t
        # try to maximize bitwise OR
        # to maximize bitwise OR, we need to get ones as left as possible
        # because a single 1 that is to the left is better than all 1's to the right
        # we can iterate from left to right and take a greedy approach
        # whatever s[i] is, we do the best we can to make it a 1

        ones, zeros = 0, 0
        for c in t:
            if c == '1':
                ones += 1
            else:
                zeros += 1

        xor_res = [] # list of '0' or '1'
        for c in s:
            if c == '1':
                # try to get zero
                if zeros > 0:
                    xor_res.append('1')
                    zeros -= 1
                else:
                    xor_res.append('0')
                    ones -= 1
            else:
                if ones > 0:
                    xor_res.append('1')
                    ones -= 1
                else:
                    xor_res.append('0')
                    zeros -= 1

        return "".join(xor_res)
