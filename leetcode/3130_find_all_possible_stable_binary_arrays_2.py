class Solution:
    def numberOfStableArrays(self, zero: int, one: int, limit: int) -> int:
        '''
        binary array is stable if 0 ct is zero, 1 ct is one, and all subarrays greater than limit must contain
        at least 1 occurrence of both 0 and 1
        zero/one control which binary arrays we can form
        len(b_arr) = zero + one

        zero=1, one=2, limit=1
        011
        101
        110
        n!/(zero!)(one!) total unique binary arrays -> return ct amongst these which are stable
        shorter subarray is limiting factor; thus requirement is same as all subarrays of length k + 1 containing both 0/1
        Let dp0 and dp1 be two 2D DP arrays where dp0[i][j] = num binary arrays with i 0's and j 1's ending in a 0
        and same for dp1
        At any point, we have 2 options. Adding a 0 or 1 to the end of the array. If we add a 0, the number of binary arrays
        able to be formed is sum of final run being k 0's where k ranges from 1..limit. This means that we basically force k 0's at the end each time, so we take the sum of dp1[i - k][j] for all such k. Same thing if we add a 1.
        Base case: all 0's or 1's for entire binary array; dp0[i][0] = 1 for i in 1..limit
        Improve to prefix sum instead of iterating zero*one*limit -> zero*one
        '''
        mod = 10**9 + 7
        zero_ct = zero
        one_ct = one
        dp0 = [[0 for _ in range(one_ct + 1)] for _ in range(zero_ct + 1)]
        dp1 = [[0 for _ in range(one_ct + 1)] for _ in range(zero_ct + 1)]
        # Base case
        for z in range(1, min(limit, zero_ct) + 1):
            dp0[z][0] = 1
        for o in range(1, min(limit, one_ct) + 1):
            dp1[0][o] = 1

        # Fill DP array
        for z in range(1, zero_ct + 1):
            for o in range(1, one_ct + 1):
                dp0[z][o] = dp0[z - 1][o] + dp1[z - 1][o] # dp0[z][o] = sum(dp1[z - k][o] for k in range(1, min(limit, z) + 1))
                # sliding window; shift left boundary if z exceeds window size
                if z - limit > 0:
                    dp0[z][o] -= dp1[z - limit - 1][o]
                dp0[z][o] %= mod

                dp1[z][o] = dp1[z][o - 1] + dp0[z][o - 1]
                if o - limit > 0:
                    dp1[z][o] -= dp0[z][o - limit - 1]
                dp1[z][o] %= mod

        return (dp0[-1][-1] + dp1[-1][-1]) % mod
