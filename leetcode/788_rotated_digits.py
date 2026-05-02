class Solution1:
    def rotatedDigits(self, n: int) -> int:
        def rotate_digit(num: int) -> int:
            digits = []
            while num > 0:
                digits.append(num % 10)
                num //= 10
            digits.reverse()

            same = set([0, 1, 8])
            invalid = set([3, 4, 7])
            change = {
                2: 5,
                5: 2,
                6: 9,
                9: 6
            }
            for i in range(len(digits)):
                if digits[i] in invalid:
                    return -1
                elif digits[i] in same:
                    continue
                digits[i] = change[digits[i]]

            return int("".join(map(str, digits)))

        res = 0
        for i in range(1, n + 1):
            rotated = rotate_digit(i)
            if rotated != -1 and i != rotated:
                res += 1

        return res


class Solution2:
    def rotatedDigits(self, n: int) -> int:
        # We can cache previous results, so that if we have x // 10 result within the array, we can use
        # newly introduced digit x % 10 to determine

        res = 0
        is_good = [0] * (n + 1) # 3 states; one for invalid, one for same, and one for good; -1, 0, 1 respectively
        same = set([0, 1, 8])
        invalid = set([3, 4, 7])
        change = set([2, 5, 6, 9])
        for i in range(1, n + 1):
            prev = i // 10
            new = i % 10
            # First deal with base cases
            if prev == 0:
                if i in change:
                    is_good[i] = 1
                    res += 1
                elif i in same:
                    is_good[i] = 0
                else:
                    is_good[i] = -1
            # Otherwise use cached result from previous computations
            else:
                if new in invalid or is_good[prev] == -1:
                    is_good[i] = -1
                elif new in change or is_good[prev] == 1:
                    is_good[i] = 1
                    res += 1

        return res
