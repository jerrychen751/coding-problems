from typing import List


# Definition for NestedInteger interface.
class NestedInteger:
    def __init__(self, value=None):
        self._is_integer = value is not None
        self._value = value
        self._list = [] if value is None else None

    def isInteger(self) -> bool:
        return self._is_integer

    def add(self, elem):
        self._list.append(elem)

    def setInteger(self, value):
        self._is_integer = True
        self._value = value

    def getInteger(self):
        return self._value if self._is_integer else None

    def getList(self):
        return None if self._is_integer else self._list


class Solution:
    def depthSumInverse(self, nestedList: List[NestedInteger]) -> int:
        # Base elements in list start at depth = 1
        # Additional layer of nesting means += 1
        # Each element is multiplied by (max_depth - element_depth + 1)
        numbers = [] # store (num, depth) where depth is 1-indexed
        def dfs(nested_int: NestedInteger, numbers: list[tuple[int, int]], depth: int) -> int:
            """Explores a nested_int fully and returns max depth of that nested integer. Also adds integer to numbers."""
            if nested_int.isInteger():
                numbers.append((nested_int.getInteger(), depth))
                return depth

            max_depth = depth
            for num in nested_int.getList():
                max_depth = max(max_depth, dfs(num, numbers, depth + 1))

            return max_depth

        max_depth = 1
        for num in nestedList:
            max_depth = max(max_depth, dfs(num, numbers, 1))

        res = 0
        for num, depth in numbers:
            res += num * (max_depth - depth + 1)

        return res
