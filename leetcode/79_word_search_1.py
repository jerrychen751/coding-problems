from typing import List


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        m = len(board)
        n = len(board[0])

        # location on board, idx in word, used positions to make word[:idx]
        # First if idx == len(word) we're done return True
        # At (i, j), first check if valid (in bounds, not used before)
        # If not, return false
        # Then check if board[i][j] == word[idx]
        # if so, try moving in each of the directions
        # if not, also return false

        def is_valid(i: int, j: int, used_pos: set[tuple[int, int]]) -> bool:
            return i >= 0 and i < m and j >= 0 and j < n and (i, j) not in used_pos

        def backtrack(i: int, j: int, idx: int, used_pos: set[tuple[int, int]]) -> bool:
            if idx == len(word):
                return True
            if not is_valid(i, j, used_pos):
                return False

            if board[i][j] != word[idx]:
                return False

            used_pos.add((i, j))
            found = (
                backtrack(i - 1, j, idx + 1, used_pos)
                or backtrack(i + 1, j, idx + 1, used_pos)
                or backtrack(i, j - 1, idx + 1, used_pos)
                or backtrack(i, j + 1, idx + 1, used_pos)
            )
            used_pos.remove((i, j))
            return found

        for i in range(m):
            for j in range(n):
                if backtrack(i, j, 0, set()):
                    return True

        return False
