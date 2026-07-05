from typing import List


class Solution:
    def stoneGameVI(self, aliceValues: List[int], bobValues: List[int]) -> int:
        values = [(aliceValues[i] + bobValues[i], i) for i in range(len(aliceValues))]
        values.sort(reverse=True)
        # values contains value of stone for whoever is actively going
        alice_score = 0
        bob_score = 0
        for i in range(len(values)):
            if i & 1 == 0:
                alice_score += aliceValues[values[i][1]]
            else:
                bob_score += bobValues[values[i][1]]

        if alice_score > bob_score:
            return 1
        if alice_score == bob_score:
            return 0

        return -1
