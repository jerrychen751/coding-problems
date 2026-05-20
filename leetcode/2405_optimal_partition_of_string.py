class Solution:
    def partitionString(self, s: str) -> int:
        seen = set()
        ct = 0
        for c in s:
            if c in seen:
                ct += 1
                seen.clear()

            seen.add(c)

        return ct + 1
