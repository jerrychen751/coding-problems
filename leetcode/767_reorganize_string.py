import heapq

class Solution:
    def reorganizeString(self, s: str) -> str:
        base = ord('a')
        freqs = [0] * 26
        for char in s:
            freqs[ord(char) - base] += 1

        max_heap = []
        for i, freq in enumerate(freqs):
            if freq == 0:
                continue

            max_heap.append((-freq, chr(base + i)))
        heapq.heapify(max_heap)

        res = []
        while max_heap:
            f1, c1 = heapq.heappop(max_heap)
            f1 = -f1
            if not max_heap:
                # Not possible b/c only 1 char left and it's > 1 freq
                if f1 > 1:
                    return ""
                # Otherwise we've popped last char
                res.append(c1)
                return "".join(res)
            else:
                # We have at least 1 more char in max_heap
                f2, c2 = heapq.heappop(max_heap)
                f2 = -f2
                res.append(c1)
                res.append(c2)
                f1 -= 1
                f2 -= 1
                if f1 > 0:
                    heapq.heappush(max_heap, (-f1, c1))
                if f2 > 0:
                    heapq.heappush(max_heap, (-f2, c2))

        return "".join(res)
