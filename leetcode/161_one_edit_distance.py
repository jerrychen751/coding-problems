class Solution:
    def isOneEditDistance(self, s: str, t: str) -> bool:
        n = len(s)
        m = len(t)
        # Case 1: More than 1 letter apart
        if abs(n - m) > 1:
            return False
        # Case 2: Both empty strings
        if n == 0 and m == 0:
            return False
        # Case 3: Same strings
        if s == t:
            return False

        edited = False # marker for whether edit has already been used
        # Since we only have one chance, we can compare until the first "mismatch"
        # Then use edit opportunity to fix immediately depending on the situation
        # If there's another mismatch, return False
        i = 0 # s
        j = 0 # t

        if abs(n - m) == 1:
            # Need to insert a character
            while i < n and j < m:
                if s[i] == t[j]:
                    i += 1
                    j += 1
                else:
                    if edited:
                        return False

                    edited = True
                    if n < m:
                        # insert char into s for t; increment t ptr
                        j += 1
                    else:
                        # insert char into t for s
                        i += 1
            # If we get through the whole while loop without edit=True, then all chars up until last char match
            # In this case we should return True
        else:
            while i < n and j < m:
                # replace one char
                if s[i] != t[j]:
                    if edited:
                        return False
                    edited = True

                i += 1
                j += 1

        return True
