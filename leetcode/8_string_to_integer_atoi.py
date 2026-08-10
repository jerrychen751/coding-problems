class Solution:
    def myAtoi(self, s: str) -> int:
        s = s.lstrip()
        if not s:
            return 0

        is_positive = (s[0] != '-')
        idx = 0 if s[0] != '+' and s[0] != '-' else 1
        val = 0

        # Skip leading zeros
        while idx < len(s) and s[idx] == '0':
            idx += 1

        while idx < len(s) and s[idx].isdigit():
            # Now we arrive at the first digit
            # After updating val, need to check if we need to clip
            val = val * 10 + int(s[idx])
            if (val > 2**31 - 1 and is_positive):
                return 2**31 - 1
            if (val > 2**31 and not is_positive):
                return -2**31

            idx += 1

        return val if is_positive else -val
