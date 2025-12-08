from math import floor, sqrt, isqrt

class Solution:
    def kthFactor(self, n: int, k: int) -> int:
        # Only need to check the first floor(sqrt(n)) numbers for factors (1st in pair)
        is_square = True if isqrt(n) ** 2 == n else False

        # Edge case: if factor ** 2 == n
        for num in range(1, floor(sqrt(n)) + 1):
            if n % num == 0:
                k -= 1
                if k == 0:
                    return num
        
        # Make a second sqrt(n) pass down for O(1) space
        if is_square:
            k += 1 # allow overcounting of the same factor twice

        for num in reversed(range(1, floor(sqrt(n)) + 1)):
            if n % num == 0:
                k -= 1
                if k == 0:
                    return n // num
        
        return -1

if __name__ == '__main__':
    s = Solution()
    print(s.kthFactor(7, 2))
