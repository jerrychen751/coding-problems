from typing import List


class Solution:
    def expand(self, s: str) -> List[str]:
        '''
        s is actually a list of words
        if letter not within curly braces, it has one representation
        if there is curly braces, entire brace is one letter with whatever letters are enclosed as options
        braces enclose different lowercase english letters, not guaranteed to be sorted

        parse word
        sort individual groups of options
        [[a,b], [c], [d, e], [f]]
        def backtrack(word: list[str], idx: int) -> None:
            if idx not in bounds: add word to resulting list
            for option in list[idx]:
                word.append(option)
                backtrack(word, idx + 1)
                word.pop()

        return resulting list
        '''
        options_list = [] # options_list[i] = options for index i of word
        words = []
        i = 0
        while i < len(s):
            if s[i].isalpha():
                options_list.append([s[i]])
                i += 1
                continue
            if s[i] == '{':
                options = []
                i += 1
                while s[i] != '}':
                    if s[i] == ',':
                        i += 1
                        continue
                    options.append(s[i])
                    i += 1
                options_list.append(options)
                i += 1

        for options in options_list:
            options.sort()

        def backtrack(word: list[str], idx: int) -> None:
            if idx >= len(options_list):
                words.append("".join(word))
                return

            for option in options_list[idx]:
                word.append(option)
                backtrack(word, idx + 1)
                word.pop()

        backtrack([], 0)
        return words
