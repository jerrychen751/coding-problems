class Solution:
    def minimumCost(self, s: str, t: str, flipCost: int, swapCost: int, crossCost: int) -> int:
        """
        Flip means we can correct 1 mismatch
        Swap means we can correct 2 mismatches if s[i] != s[j] or t[i] != t[j]
        Cross means we can invert both s[i] and t[i]; mismatch is still there but can followup w/ swap

        If 1 mismatch, doesn't make sense to cross or swap
        If 2 mismatches:
            let i, j be mismatched indices
            if s[i] == s[j]:
                perform min(cross + swap, flip twice)
            else:
                perform min(swap, flip twice)

        Iterate through s/t in order
            if match, continue
            if mismatches up to now are odd, then keep going
            if mismatches up to now are even, perform action then reset

        check mismatches if odd flip one time at end
        """
        mismatches = 0
        n = len(s)

        # Collect list of all mismatches, pair up all 0's and 1's possible for swap and compare flip twice vs. swap
        # For remaining of same value, decrement pairs and compare flip twice vs. cross + swap
        # If 1 remaining, then flip

        x, y = 0, 0 # number of mismatches where s[i] == '0' and s[i] == '1'
        for i in range(n):
            if s[i] != t[i]:
                if s[i] == '0':
                    x += 1
                else:
                    y += 1

        cost = 0
        matches = min(x, y)
        remainder = max(x, y) - matches

        # First compare swap alone
        cost += min(matches * swapCost, matches * 2 * flipCost)
        # Then deal w/ remainder
        # First ensure it's even; flip if it's odd to make it even
        if remainder % 2 == 1:
            remainder -= 1
            cost += flipCost

        # Then compare flipping all vs. cross + swap
        cost += min(remainder * flipCost, (remainder // 2) * (crossCost + swapCost))

        return cost
