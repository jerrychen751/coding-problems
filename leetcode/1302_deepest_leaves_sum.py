from collections import deque
from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def deepestLeavesSum(self, root: Optional[TreeNode]) -> int:
        # BFS level order traversal
        # Use a queue and process each level sequentially
        # Pop 1 level at a time from the queue, and then add children to queue if they're not None
        # Track number of children added and curr sum of level
        # If num_children = 0 return curr sum we're done
        if root is None:
            return 0

        queue = deque([root])
        while len(queue) > 0:
            level_sum = 0
            num_children = 0
            for _ in range(len(queue)):
                curr = queue.popleft()
                if curr.left is not None:
                    queue.append(curr.left)
                    num_children += 1
                if curr.right is not None:
                    queue.append(curr.right)
                    num_children += 1
                level_sum += curr.val

            if num_children == 0:
                return level_sum

        return 0
