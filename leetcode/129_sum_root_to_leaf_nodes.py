from collections import deque
from typing import Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

        
class Solution:
    def sumNumbers(self, root: Optional[TreeNode]) -> int:
        # we want the sum of all paths from root -> left
        # nodes in the path form digits; sum each path
        # node.val is between 0 and 9

        # approach
        # track a total sum
        # bfs for level order traversal; for each node at each level we have a path built out so far
        # add sum to total if we see that it has no children (leaf node)
        if not root:
            return 0

        total = 0
        queue = deque([(root, root.val)]) # store (node, path)
        while len(queue) > 0:
            node, path = queue.popleft()

            # Check if node is a leaf
            if node.left is None and node.right is None:
                total += path
                continue
            
            if node.left is not None:
                queue.append((node.left, path * 10 + node.left.val))
            if node.right is not None:
                queue.append((node.right, path * 10 + node.right.val))
        
        return total