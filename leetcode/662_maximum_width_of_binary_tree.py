from collections import deque
from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def widthOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        # Say root has height = 0
        # At height h, there are at most 2**h nodes in the binary tree at that level
        # The width at any level, if we were to represent it as an index, is the largest idx - smallest idx
        # which is filled in an array of length 2**h

        # Say that the "index" position of a node at height h is i
        # Then their left child at height h+1 has index 2*i, right child at height h+1 has index 2*i + 1
        # If we perform level-order BFS traversal, and we store (node, node_idx)
        # Then their child is at node_idx * 2 if left, node_idx * 2 + 1 if right
        # And then when we process a level, we first compute first and last nodes in that level
        # which is leftmost and rightmost, so then we determine (queue[-1][1] - queue[0][1] + 1) as that level's width
        # take max width at each level

        queue = deque([(root, 0)])
        max_width = 0
        while queue:
            width = queue[-1][1] - queue[0][1] + 1
            max_width = max(max_width, width)
            for _ in range(len(queue)):
                curr, curr_idx = queue.popleft()
                if curr is None:
                    continue

                if curr.left is not None:
                    queue.append((curr.left, 2 * curr_idx))
                if curr.right is not None:
                    queue.append((curr.right, 2 * curr_idx + 1))

        return max_width
