from typing import List


class Solution:
    def stoneGameVII(self, stones: List[int]) -> int:
        # Since all stones are positive, Alice will always win since she goes first
        # Bob wants to min score diff
        # Alice wants to max score diff
        # Each player can remove from left/right side

        # Initial thought is greedy; since Alice will win no matter what Bob should maximize his score
        # However if he simply picks the smaller of either side it may lead to Alice gaining even more points next turn
        # We simply have to simulate paths, since at each step they can either remove from left or right
        # Keep running sum of stones. On each person's turn, their score increases by curr_sum - removed_stone
        # We cache index range of values, i.e., there are multiple ways for it to be Alice/Bob's turn with indices 1-4 (0 and 5 are removed, with either A=0, B=5 or A=5, B=0, etc).

        n = len(stones)
        pref_sum = [0] * (n + 1) # pref_sum[i] = sum(stones[:i])
        for i in range(n):
            pref_sum[i + 1] = pref_sum[i] + stones[i]

        dp = [[float('inf') for _ in range(n)] for _ in range(n)]
        # dp[start][end] stores difference game w/ stones[start:end + 1]
        # num stones removed is start + (n - end - 1)
        # if this is even, it's alice's turn, otherwise bob (no overlap)

        def find_difference(start: int, end: int, alice_turn: bool) -> int:
            """Returns alice_score - bob_score for the game which starts at stones[start:end + 1] with alice_turn indicating who's turn it was."""
            # Base case
            if start == end:
                return 0

            # Use dp
            if dp[start][end] != float('inf'):
                return dp[start][end]

            # Calculate score depending on action
            rm_start_score = pref_sum[end + 1] - pref_sum[start + 1]
            rm_end_score = pref_sum[end] - pref_sum[start]

            if alice_turn:
                # we want to return max possible difference
                # add because prev (alice - bob) started on bob's turn
                # now alice's score increases so gap increases
                diff = max(
                    find_difference(start + 1, end, not alice_turn) + rm_start_score,
                    find_difference(start, end - 1, not alice_turn) + rm_end_score
                )
                dp[start][end] = diff
                return diff
            else:
                # subtract because now it's bob's turn, so gap between previous
                # (alice - bob) will decrease
                diff = min(
                    find_difference(start + 1, end, not alice_turn) - rm_start_score,
                    find_difference(start, end - 1, not alice_turn) - rm_end_score
                )
                dp[start][end] = diff
                return diff

        return abs(find_difference(0, n - 1, True))
