"""
Failed Attempt — tried to simulate inversions greedily with a min-heap, picking the most negative element and inverting with its smallest adjacent. Doesn't work in general because local greedy choices interact across the board.

Correct insight (used below): the parity of the negative count is invariant under adjacent-pair inversions, and negative signs can "move" freely. So the answer is just sum(abs(x)) for the whole matrix when neg_ct is even, minus 2 * min_abs when it's odd.

import heapq

class Solution:
    def maxMatrixSum(self, matrix: List[List[int]]) -> int:
        # Equivalent to saying, can we make the largest number of negative values positive
        # Return the sum after conversions

        # If we have a large negative number (larger than any adj element), we should always convert it w/ smallest adj element
        # smallest works for both neg/pos; if negative that's great, if positive, we still gain a greater sum overall

        # Any positive element with >= 2 negative adj can turn negatives into positives
        # Order matters, but there's symmetry
        # Due to the property that we can only invert pairs, we are guaranteed two types of actions
        # The first is if there's a negative number, we check two things:
            # Is there a largest negative number adj to it, if so, travel in that dir

        # Plan
        # Use a min-heap to store (element, i, j) where (i, j) is location within matrix for all negative elements
        # we process these elements one at a time, starting with most negative
        # We apply the idea of invert w/ smallest adj element, so long as -(adj)-(element) > 0
        # Continue processing; because we may have inverted another negative in this process, if for any element matrix[i][j] is
        # already positive, then we continue onto next (inverted by some previous change)
        # On the first pass through the matrix, we obtain an initial sum value
        # As we process, we adjust that sum value by -(adj)-(element)

        min_heap = []
        n = len(matrix)
        res = 0
        for i in range(n):
            for j in range(n):
                x = matrix[i][j]
                res += x
                if x < 0:
                    heapq.heappush(min_heap, (x, i, j))

        dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        while len(min_heap) > 0:
            # Get min adj element to this negative number
            x, i, j = heapq.heappop(min_heap)

            # If matrix[i][j] > 0, then it was affected by a previous invert and is now positive -> no need to process anymore
            if matrix[i][j] > 0:
                continue

            min_adj = float('inf')
            adj_i, adj_j = 0, 0
            for di, dj in dirs:
                new_i, new_j = i + di, j + dj
                if not self.in_bounds(n, new_i, new_j):
                    continue

                if matrix[new_i][new_j] < min_adj:
                    adj_i = new_i
                    adj_j = new_j
                    min_adj = matrix[new_i][new_j]

            # Decide whether to invert or not
            delta = 0 - min_adj - x
            if delta <= 0:
                # Decide not to invert
                continue

            # Otherwise, we invert the pair and then deal with the aftereffects of inverting the other number
            # If originally negative, it's now positive and when we pop this entry from the heap we do nothing
            # If zero, nothing happens
            # Otherwise, turn it negative and push to heap to be processed later
            matrix[adj_i][adj_j] = -min_adj
            if min_adj > 0:
                heapq.heappush(min_heap, (-min_adj, adj_i, adj_j))

            # Deal with the change in res
            res += delta

        return res

    def in_bounds(self, n: int, i: int, j: int) -> bool:
        return i >= 0 and i < n and j >= 0 and j < n
"""
from typing import List


class Solution:
    def maxMatrixSum(self, matrix: List[List[int]]) -> int:
        # Key insight: Parity of # of negatives doesn't change
        # By inverting adjacent pairs, negative signs can "move" throughout the matrix
        # And we can always force pairs as long as there's > 1 negative sign present
        # A negative pair becomes wholly positive

        # In this paradigm, any matrix with an even number of negatives becomes entirely positive, so we return sum of abs(matrix[i][j]) for each i,j index
        # For any odd number, we can "sacrifice" the smallest abs value to act as the negative value to maximize the sum
        n = len(matrix)
        res = 0
        neg_ct = 0
        min_abs = float('inf')
        for i in range(n):
            for j in range(n):
                x = matrix[i][j]
                res += abs(x)
                if x < 0:
                    neg_ct += 1
                min_abs = min(min_abs, abs(x))

        if neg_ct % 2 == 0:
            return res

        return res - 2 * min_abs # account for "overcounting" smallest abs value
        # minus once to cancel out addition, again for actual subtraction
