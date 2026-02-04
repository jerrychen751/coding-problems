class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        # want to find length of longest substring without duplicate characters

        # can input string be empty?
        # is w and W considered duplicate? case sensitivity?

        # approach
        # track left and right pointers of a sliding window across the string (inclusive bounds)
        # length of some valid substring is difference between the pointers + 1
        # have a hash map tracking characters seen within the window, mapping char to idx in string
            # when expanding right side of window, if new char at s[right] not in hash map, we add to hash map
            # and continue expanding rightward
            # if new char s[right] is in hash map, then we find location of duplicate via map lookup
            # and then we remove all chars from left...duplicate from the hash map (cannot proceed any further)
        # at the end of each window expansion, calculate new size of substring and update max_len if needed

        if len(s) == 0:
            return 0

        max_len = 1
        left, right = 0, 1
        window = {s[0]: 0} # char: idx
        while right < len(s):
            newchar = s[right]
            if newchar not in window:
                window[newchar] = right
                max_len = max(max_len, right - left + 1)
                right += 1
            else:
                newleft = window[newchar] + 1
                while left < newleft:
                    del window[s[left]]
                    left += 1
            
                max_len = max(max_len, right - left + 1)

        return max_len
            