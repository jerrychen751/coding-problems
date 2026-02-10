from collections import deque
from typing import Optional, List

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

        
class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        # Perform BFS; take the rightmost element on each level and add to result
        if not root:
            return []

        res = [root.val]
        queue = deque([root])
        while len(queue) > 0:
            n = len(queue) # size of level
            for _ in range(n):
                curr = queue.popleft()
                if curr.left is not None:
                    queue.append(curr.left)
                if curr.right is not None:
                    queue.append(curr.right)
            
            # Alternatively we can check if idx in for loop iteration is equal to n - 1, to record the last processed element per lvl
            if len(queue) > 0:
                rightmost = queue[-1] # as each level is added to queue, the rightmost in that level is recorded
                res.append(rightmost.val)

        return res
