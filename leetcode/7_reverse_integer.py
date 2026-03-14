# from collections import deque

class Solution:
    def reverse(self, x: int) -> int:
        is_negative = x < 0
        x = abs(x)

        # Remove trailing zeros
        while x > 0 and x % 10 == 0:
            x //= 10

        i = 0 # counter for place
        res = 0
        bound = 2**31 if is_negative else 2**31 - 1
        
        while x > 0:
            digit = x % 10

            # Check for overflow
            # Condition is res * 10 + digit <= bound
            # This way, current res isn't overflowing, and right side has only decreased from bound
            # In other words res <= (bound - digit) / 10
            if res > (bound - digit) / 10:
                return 0

            res = res * 10 + digit
            x //= 10

        return -res if is_negative else res

        

        '''
        res = deque([])
        n = str(x)
        is_negative = n[0] == '-'
        for char in reversed(n):
            if char.isnumeric():
                res.append(char)
        
        # Remove leading zeros
        while len(res) > 1 and res[0] == '0':
            res.popleft()

        flipped = ''.join(res)
        
        def in_bounds(num: str, is_negative: bool) -> bool:
            MAX_BOUND = str(2**31) if is_negative else str(2**31 - 1)

            # Regardless of whether positive or negative, if lengths don't match, we can exit early
            if len(num) < len(MAX_BOUND):
                return True
            elif len(num) > len(MAX_BOUND):
                return False
            
            for i in range(len(num)):
                if num[i] > MAX_BOUND[i]:
                    return False
                elif num[i] < MAX_BOUND[i]:
                    return True
            
            return True

        if in_bounds(flipped, is_negative):
            return int('-' + flipped) if is_negative else int(flipped)
        else:
            return 0
        '''