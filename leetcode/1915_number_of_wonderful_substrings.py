class Solution:
    def wonderfulSubstrings(self, word: str) -> int:
        # Notes
        # String is wonderful as long as frequency of distinct chars are even, with 1 exception allowed
        # Want to return the number of substrings which are considered wonderful

        # All individual letters can contribute to this count
        
        # Approach
        # Iterate through all letters of the word (possible starts for substring)
            # Form a window, expand this window until end of word, increment a wonderful ct

        # O(n^2) time

        # Issue is that if a specific substring already has more than 2 letters appearing w/ odd freq, then no need to expand more
        # We don't know when to expand window vs. decrease window size

        # prefixes[i] stores prefix ending at i-th index (inclusive)
        # ultimately, we want bitmasks of all 0's or a single 1 (can iterate through possible positions for 1s and add)
        # maintain hash map mapping prefix -> count

        # Insight 1: parity of s[l + 1...r] = prefixes[l] ^ prefixes[r]
        # where prefixes[i] stores the bitmask encoding whether letters are even/odd of the prefix ending at index i
        # Insight 2: prefixes[l] ^ prefixes[r] can be all 0's or have a single 1 at some bit position

        count = [0] * 1024
        count[0] = 1
        mask = 0
        res = 0

        for c in word:
            mask ^= 1 << (ord(c) - ord('a')) # indicates change in parity of specific char; 10-bit mask indicates parity of chars
            res += count[mask] # case where prefixes[l] ^ prefixes[r] is all 0's (same bitmask)
            # also, having count[0] = 1 at the beginning properly counts cases where the whole prefix is all even char freqs

            for bit in range(10):
                target = 1 << bit
                
                # We want prefixes[l] ^ prefixes[r] == target
                # => prefixes[l] = target ^ prefixes[r]
                res += count[target ^ mask]
            
            count[mask] += 1
        
        return res