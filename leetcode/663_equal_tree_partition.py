from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def checkEqualTree(self, root: Optional[TreeNode]) -> bool:
        # By removing exactly one edge, we're basically saying sub of subtree will equal sum of remainder of original tree
        # But how will we know whether subtree sum equals remainder of tree?
        # Subtree sum means postorder traversal, but this also means that we won't know sum of rest of tree
        # But because they must be equal, we can simply check whether subtree sum is sum(tree) // 2

        # First obtain sum of whole tree, then set that as target
        # Then perform postorder
        # Alternatively build a set of subtree sums
        # And then at the end take the sum of whole tree, divide by 2, and find if it's in that set

        def dfs(curr: Optional[TreeNode]) -> int:
            if curr is None:
                return 0

            left_sum = dfs(curr.left)
            right_sum = dfs(curr.right)
            return left_sum + right_sum + curr.val

        total = dfs(root)
        if total & 1 == 1:
            return False

        target = total // 2

        def can_reach_target(curr: Optional[TreeNode]) -> tuple[int, bool]:
            """Return whether curr is root of a binary tree summing to target."""
            if curr is None:
                return 0, False

            left_sum, left_reach_target = can_reach_target(curr.left)
            right_sum, right_reach_target = can_reach_target(curr.right)
            total = left_sum + right_sum + curr.val
            if left_reach_target or right_reach_target:
                return total, True
            if curr.left is not None and left_sum == target or curr.right is not None and right_sum == target:
                return total, True

            return total, False

        total, can_reach = can_reach_target(root)
        return can_reach
