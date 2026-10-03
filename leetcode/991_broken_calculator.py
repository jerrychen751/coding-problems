class Solution:
    def brokenCalc(self, startValue: int, target: int) -> int:
        '''
        Two options: multiply by 2 or subtract 1
        If target < startValue, can only subtract so take difference

        Doubling every time toward larger target isn't reliable
        Each forward path has backward path w/ reverse operations of same length

        Let x be curr number in backward path, s be startValue
        If x > s and x is odd, we must add 1 then divide by 2
        If x > s and x is even, we could divide immediately or add first then divide

        (x // 2) + 1
        (x + 1 + 1) // 2 -> x//2 + 1
        We should always divide first when we're able to
        '''
        if target < startValue:
            return startValue - target

        curr = target
        moves = 0
        while curr > startValue:
            moves += 1
            if curr % 2 == 1:
                curr += 1
            else:
                curr //= 2

        return moves + (startValue - curr)
