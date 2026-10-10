class Solution:
    def minCost(self, startPos: list[int], homePos: list[int], rowCosts: list[int], colCosts: list[int]) -> int:
        s_i, s_j = startPos
        t_i, t_j = homePos

        vertical_cost = sum(rowCosts[s_i + 1:t_i + 1]) if s_i <= t_i else sum(rowCosts[t_i:s_i])
        horizontal_cost = sum(colCosts[s_j + 1:t_j + 1]) if s_j <= t_j else sum(colCosts[t_j:s_j])
        return vertical_cost + horizontal_cost
