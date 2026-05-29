class Solution:
    def tribonacci(self, n: int) -> int:
        base = [0, 1, 1]
        if n <= 2:
            return base[n]

        first = 0
        mid = 1
        last = 1
        kth_tribonacci = 2
        k = 3
        while k < n:
            first = mid
            mid = last
            last = kth_tribonacci
            kth_tribonacci = first + mid + last
            k += 1

        return kth_tribonacci
