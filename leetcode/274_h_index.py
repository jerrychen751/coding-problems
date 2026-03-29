from typing import List

class Solution:
    def hIndex(self, citations: List[int]) -> int:
        limit = len(citations)
        buckets = [0] * (limit + 1) # buckets[i] indicates number of papers with i citations

        for c in citations:
            buckets[min(c, limit)] += 1
        
        h_idx = 0
        total_ct = 0
        for i in range(len(buckets) - 1, -1, -1):
            total_ct += buckets[i] # number of papers with i or more citations
            h_idx = max(h_idx, min(total_ct, i))
        
        return h_idx

        """
        # max possible h_idx = min(len(citations), max(citations))

        # Sort the citations array
        # [0, 1, 3, 5, 6]
        
        # h_idx is the largest min(i, citations_ct[i])

        citations.sort(reverse=True)
        h_idx = 0
        for i, c in enumerate(citations):
            h_idx = max(h_idx, min(i + 1, c))

        return h_idx
        """