from collections import deque
from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def addOneRow(self, root: Optional[TreeNode], val: int, depth: int) -> Optional[TreeNode]:
        if depth == 1:
            new_root = TreeNode(val, root)
            return new_root
        if root is None:
            return None

        curr_depth = 1 # depth of current level we're processing
        queue = deque([root])

        for _ in range(depth - 2):
            for _ in range(len(queue)):
                curr = queue.popleft()
                if curr.left is not None:
                    queue.append(curr.left)
                if curr.right is not None:
                    queue.append(curr.right)

        for node in queue:
            node.left = TreeNode(val, left=node.left)
            node.right = TreeNode(val, right=node.right)

        return root
