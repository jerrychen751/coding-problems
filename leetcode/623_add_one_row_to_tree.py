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

        curr_depth = 1 # depth of current level we're processing
        queue = deque([root])

        while queue:
            for _ in range(len(queue)):
                node = queue.popleft()
                if node is None:
                    continue

                if curr_depth == depth - 1:
                    child = TreeNode(val, node.left, None)
                    old_child = node.left
                    node.left = child
                    queue.append(old_child)
                else:
                    queue.append(node.left)

                if curr_depth == depth - 1:
                    child = TreeNode(val, None, node.right)
                    old_child = node.right
                    node.right = child
                    queue.append(old_child)
                else:
                    child = node.right
                    queue.append(node.right)

            if curr_depth == depth - 1:
                break
            curr_depth += 1

        return root
