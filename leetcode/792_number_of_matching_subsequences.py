from collections import defaultdict
from bisect import bisect_left
from typing import List

class Solution:
    def numMatchingSubseq(self, s: str, words: List[str]) -> int:
        # Given a string and an array of words, return the number of elements in words that are a subsequence of s
        
        # Naive solution
        # For each word in words, iterate through s and see if letters match up sequentially
        # If the pointer in words[i] reaches the end, then we know it's a subsequence and increment a counter
        # If n = len(s) and m = len(words), this would be O(m * n)

        # Ideas
        # Map letters in s to their index, so we have letters[char] = list of indices
        # Iterate through each word in words
        # For each word, iterate through their letters and perform lookup in map, tracking curr_idx which
        # represents the index within s (i.e., index of last accepted letter)
        
        letters = defaultdict(list)
        for i in range(len(s)):
            letters[s[i]].append(i)

        res = 0
        for word in words:
            curr_idx = -1 # idx we are at in s to find the last used char
            for char in word:
                # s doesn't even contain letter, so we exit immediately
                if char not in letters:
                    break
                
                pos = bisect_left(letters[char], curr_idx + 1) if curr_idx != -1 else 0
                if pos >= len(letters[char]):
                    break
                curr_idx = letters[char][pos]
            else:
                res += 1
        
        return res

# A cleaner approach would've been to obtain an iterator for each word in words. And then store a hash map of 26 letters mapping to list of iterators of words.
# Loop through each char in s, and for that char, advance all of the iterators within that letter's bucket.