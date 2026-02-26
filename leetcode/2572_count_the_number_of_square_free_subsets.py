from typing import List

class Solution:
    def squareFreeSubsets(self, nums: List[int]) -> int:
        # Square-free integer means it's not divisible by a square number
        # Subset of array nums is square-free if the product of its elements are square-free
        # Return number of square-free non-empty subsets mod (10**9 + 7)

        # If a number is a perfect square, it must be deleted
        # No two numbers can share the same factors in subset
        # Numbers in nums is limited to 30 or less
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] # indices 0...9 represent first 10 primes
        # There are 2^10 possible states
        
        def build_prime_mask(num: int, primes: list[int]) -> int:
            """Return prime bitmask of number, or -1 if it is a perfect square."""
            mask = 0
            for i, p in enumerate(primes):
                if num % p == 0:
                    num //= p
                    if num % p == 0:
                        return -1
                    mask |= (1 << i)
            
            return mask
        
        # Non-empty subset is considered distinct as long as deleted indices are different
        # 1 is special -> constributes multiplicative factor of 2^k where k is number of 1's

        # A number is valid curr & mask == 0 (no shared primes)
        # dp[mask] stores number of subsets which fulfills that mask state
        ones = 0 # treat ones separately
        dp = [0] * (2**len(primes))
        dp[0] = 1 # base case
        for num in nums:
            if num == 1:
                ones += 1
                continue

            m = build_prime_mask(num, primes)
            if m == -1:
                continue

            # Determine whether to include or exclude
            for mask in range(len(dp) - 1, -1, -1):
                if m & mask == 0:
                    new_mask = m | mask
                    dp[new_mask] += dp[mask]
        
        total = sum(dp) % (10**9 + 7)
        total = (total * (2**ones)) % (10**9 + 7)
        return (total - 1) % (10**9 + 7)
                