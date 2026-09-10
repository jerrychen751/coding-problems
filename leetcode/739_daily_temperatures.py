from typing import List


class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        '''
        Return res so that res[i] is (j - i) where j is temp[j] > temp[i]
        0 <= i < j; temp[i] < temp[j]
        Iterate in reverse order
        Monotonic stack of indices (decreasing in temp value)
        for some i, if temp[stack[-1]] <= temp[i] we pop
            if stack is empty, there is no warmer temperature to the right -> res[i] = 0
            if stack not empty, res[i] = stack[-1] - i
            append i to stack

        return res
        '''
        stack = []
        n = len(temperatures)
        res = [0] * n
        for i in range(n - 1, -1, -1):
            while stack and temperatures[stack[-1]] <= temperatures[i]:
                stack.pop()

            if stack:
                res[i] = stack[-1] - i

            stack.append(i)

        return res
