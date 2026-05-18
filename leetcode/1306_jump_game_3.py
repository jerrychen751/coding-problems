from typing import List


class Solution1:
    def canReach(self, arr: List[int], start: int) -> bool:
        # Take a dfs approach
        # Can either modify input array to show visited, or use another array/set
        seen = [False] * len(arr)

        def dfs(curr: int, seen: List[bool]) -> bool:
            if curr < 0 or curr >= len(arr):
                return False
            if seen[curr]:
                return False

            seen[curr] = True
            if arr[curr] == 0:
                return True

            return dfs(curr + arr[curr], seen) or dfs(curr - arr[curr], seen)

        return dfs(start, seen)


class Solution2:
    def canReach(self, arr: List[int], start: int) -> bool:
        # Try for iterative DFS
        seen = [False] * len(arr)
        stack = [start] # indices to explore
        while len(stack) > 0:
            curr = stack.pop()
            if curr < 0 or curr >= len(arr):
                continue
            if seen[curr]:
                continue

            seen[curr] = True
            if arr[curr] == 0:
                return True
            stack.append(curr - arr[curr])
            stack.append(curr + arr[curr])

        return False
