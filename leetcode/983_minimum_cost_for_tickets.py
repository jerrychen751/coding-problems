from typing import List


class Solution:
    def mincostTickets(self, days: List[int], costs: List[int]) -> int:
        # min cost to travel in days leading up to days[i]
        # try each of the costs
        # Let dp[i] represent min cost to travel days[:i]

        def get_cost(dp: list[int], idx: int, interval: int) -> int:
            """Return dp[j] where j is first index > days[i] - interval."""
            j = idx
            for i in range(idx - 1, -1, -1):
                if days[i] > days[idx] - interval:
                    j = i
                else:
                    break

            return dp[j]

        # At each step, we choose a ticket to get
        # total cost to cover 0..i days is min of cost of getting 3 tickets
        # each ticket is the price of days[:j] + costs[0/1/2] where j is the rightmost index which is <= days[i] - 1/7/30
        n = len(days)
        dp = [0] * (n + 1)
        for i in range(n):
            cost1 = get_cost(dp, i, 1) + costs[0]
            cost7 = get_cost(dp, i, 7) + costs[1]
            cost30 = get_cost(dp, i, 30) + costs[2]
            best = min(cost1, cost7, cost30)
            dp[i + 1] = best

        return dp[-1]
