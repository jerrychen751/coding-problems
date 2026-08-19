from typing import List


class Solution:
    def stoneGame(self, piles: List[int]) -> bool:
        '''
        n = len(piles)
        n is even
        sum(piles) is odd -> no ties

        greedy? take pile with most stones each turn
        sort pile
        even indices belong to Alice, odd indices belong to Bob
        '''
        return True
