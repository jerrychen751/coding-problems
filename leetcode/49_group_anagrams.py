from typing import List


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # Sort each word -> use hash map mapping key : list of strings
        # where key is sorted form of word (anagrams share same key)

        # Another method of obtaining key is just to count number of each letter instead of sorting each word
        # Then the key becomes a sequence of char frequencies of length 26 (a-z)
        # How do we know how to group the same words? Still need a hash map mapping key to list of words in that group
        key_to_words = {}
        for word in strs:
            freqs = [0] * 26
            for char in word:
                idx = ord(char) - ord('a')
                freqs[idx] += 1

            key = tuple(freqs)
            if key in key_to_words:
                key_to_words[key].append(word)
            else:
                key_to_words[key] = [word]

        return [v for v in key_to_words.values()]
