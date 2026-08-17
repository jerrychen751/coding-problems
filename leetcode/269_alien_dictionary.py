from collections import defaultdict, deque
from typing import List

class Solution:
    def alienOrder(self, words: List[str]) -> str:
        '''
        words are sorted lexicographically in rules of the language
        claim may be incorrect
        if incorrect, return ""
        if correct return string of letters in alien language sorted by their rules

        words consists of lowercase english letters
        duplicate words? yes
        1:1 correspondence
        shorter word comes earlier if entire length of shorter word matches up

        w e r
        t f
        r t

        w -> e -> r -> t -> f
        DAG
        if invalid, can we detect that with cycle in DAG? yes
        topological sort

        graph = defaultdict(list)
        degree = {char: 0 for word in words for char in word}
        for l, r in zip(words, words[1:]):
            max_len = min(len(l), len(r))
            idx = 0
            while idx < max_len and l[idx] == r[idx]:
                idx += 1
            # either letters are different at idx or we've exceeded length of one word
            if idx < max_len:
                if idx < len(l):
                    return ""
            else:
                graph[l[idx]].append(r[idx])
                degree[r[idx]] += 1

        queue = deque([c for c, d in degree.items() if d == 0])
        sequence = []
        while queue:
            curr = queue.popleft()
            sequence.append(curr)
            for neighbor in graph[curr]:
                degree[neighbor] -= 1
                if degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(sequence) == len(degree):
            return sequence
        return ""
        '''
        graph = defaultdict(list)
        degree = {char: 0 for word in words for char in word}
        for l, r in zip(words, words[1:]):
            max_len = min(len(l), len(r))
            idx = 0
            while idx < max_len and l[idx] == r[idx]:
                idx += 1
            # either letters are different at idx or we've exceeded length of one word
            if idx >= max_len:
                if idx < len(l):
                    return ""
            else:
                graph[l[idx]].append(r[idx])
                degree[r[idx]] += 1

        queue = deque([c for c, d in degree.items() if d == 0])
        sequence = []
        while queue:
            curr = queue.popleft()
            sequence.append(curr)
            for neighbor in graph[curr]:
                degree[neighbor] -= 1
                if degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(sequence) == len(degree):
            return "".join(sequence)
        return ""
