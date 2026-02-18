from collections import Counter
from typing import List

class Solution:
    def subdomainVisits(self, cpdomains: List[str]) -> List[str]:
        freqs = Counter()
        res = []
        for item in cpdomains:
            ct, domain = item.split()
            ct = int(ct)

            while True:
                freqs[domain] += ct
                dot_idx = domain.find('.')

                if dot_idx == -1:
                    break
                domain = domain[dot_idx + 1:]
            
        for k, v in freqs.items():
            res.append(' '.join([str(v), k]))
        
        return res