from functools import cache
from typing import List, Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def allPossibleFBT(self, n: int) -> List[Optional[TreeNode]]:
        # return a list of references to root of possible full binary trees
        # values should all be 0
        
        # structure must be different
        # if n is even, the tree cannot be full, then we return an empty list
        
        if n % 2 == 0:
            return []
        
        @cache
        def dp(n_remaining: int) -> list[TreeNode]:
            if n_remaining == 1:
                return [TreeNode(0)]
            
            trees = []
            for l_size in range(1, n_remaining, 2):
                r_size = n_remaining - l_size - 1 # -1 for root node; included in n_remaining
                l_subtrees = dp(l_size)
                r_subtrees = dp(r_size)
                for l in l_subtrees:
                    for r in r_subtrees:
                        root = TreeNode(0)
                        root.left = l
                        root.right = r
                        trees.append(root)
            
            return trees
    
        return dp(n)
