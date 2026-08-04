from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def convertBST(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        # post-order traversal
        # def dfs(curr) -> int
        # Base case is if curr is None, return 0
        # change curr node val in-place to be curr.val + dfs(curr.right)
        # return curr.val + left subtree sum + right subtree sum

        stack = []
        curr = root
        greater_sum = 0 # tracker for sum of all tree values greater than curr node at top of stack
        while stack or curr is not None:
            while curr is not None:
                stack.append(curr)
                curr = curr.right

            curr = stack.pop()
            greater_sum += curr.val
            curr.val = greater_sum
            curr = curr.left

        return root
