class Solution:
    def isLongPressedName(self, name: str, typed: str) -> bool:
        # Go with a greedy solution
        # Keep indices i, j as pointers into name and typed
        # Keep a prev variable tracking prev char from name
        # At any typed[j], there are 3 possibilities
        # If name[i] == typed[j], then always take the match and increment both pointers
        # If name[i] != typed[j] but prev == typed[j], give benefit of the doubt and increment j
        # If name[i] != typed[j] and prev != typed[j], return False right there
        # Continue this while i/j are within bounds of string length
        # After going out of bounds, there are 2 possibilities
        # i in bounds, j out -> False
        # i out, j in -> True if all letters remaining are same as prev otherwise False
        # both out -> True

        n, m = len(name), len(typed)
        i, j = 0, 0
        prev_name_char = None
        while i < n and j < m:
            if name[i] == typed[j]:
                prev_name_char = name[i]
                i += 1
                j += 1
            else:
                if prev_name_char == typed[j]:
                    j += 1
                else:
                    return False


        if i >= n and j >= m:
            return True # complete both exactly
        if i >= n and all([typed[k] == prev_name_char for k in range(j, m)]):
            return True

        return False
