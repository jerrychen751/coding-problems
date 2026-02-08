from typing import List

class Solution:
    def getFolderNames(self, names: List[str]) -> List[str]:
        seen = {} # basename: ct
        res = []
        for name in names:
            if name not in seen:
                seen[name] = 1
                res.append(name)
            else:
                ct = seen[name]
                candidate = name + f"({ct})"
                while candidate in seen:
                    ct += 1
                    candidate = name + f"({ct})"
                seen[name] = ct + 1
                seen[candidate] = 1
                res.append(candidate)
        
        return res