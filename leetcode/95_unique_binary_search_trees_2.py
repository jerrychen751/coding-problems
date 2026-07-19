from functools import cache
from typing import List, Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Definition for a binary tree node.
# class TreeNode:
#     def **init**(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def generateTrees(self, n: int) -> List[Optional[TreeNode]]:
        if n == 0:
            return []

        @cache
        def backtrack(low: int, high: int) -> list[Optional[TreeNode]]:
            """Return a list of all subtrees able to be build with (high - low + 1) number of nodes."""
            if high < low:
                return [None]
            if low == high:
                return [TreeNode(low)]
            
            trees = []
            for root in range(low, high + 1):
                left_subtrees = backtrack(low, root - 1)
                right_subtrees = backtrack(root + 1, high)
                # Cartesian product of possible trees
                for l_tree in left_subtrees:
                    for r_tree in right_subtrees:
                        trees.append(TreeNode(root, l_tree, r_tree))
                
            return trees
        
        return backtrack(1, n)
