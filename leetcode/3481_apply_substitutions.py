from collections import deque, defaultdict
from typing import List

class Solution:
    def applySubstitutions(self, replacements: List[List[str]], text: str) -> str:
        '''
        replacements is list of original, replacement pairs
        text contains %var% placeholders where var is original; needs to get replaced (with percentage signs) into replacement

        nested values? %var1%var2%% -> no; placeholders in text correspond to a unique key which is a single uppercase letter
        however, value in replacements can contain placeholders

        resolve replacements mapping upfront, then perform simple substitution in the text
        DFS to resolve dependencies
        '''
        mapping = {k: v for k, v in replacements}
        resolved = {}

        def expand(val: str) -> str:
            res = []
            idx = 0
            while idx < len(val):
                if val[idx] == '%':
                    key = val[idx + 1]
                    res.append(resolve(key))
                    idx += 3
                else:
                    res.append(val[idx])
                    idx += 1

            return "".join(res)

        def resolve(key: str) -> str:
            if key in resolved:
                return resolved[key]

            resolved[key] = expand(mapping[key])
            return resolved[key]

        return expand(text)
