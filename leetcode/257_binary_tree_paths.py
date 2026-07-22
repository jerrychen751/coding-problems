from typing import List, Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def binaryTreePaths(self, root: Optional[TreeNode]) -> List[str]:
        root_to_leaf_paths = []
        def backtrack(curr: Optional[TreeNode], path: list[str]) -> None:
            if curr is None:
                return

            path.append(str(curr.val))
            if curr.left is None and curr.right is None:
                root_to_leaf_paths.append("->".join(path.copy()))
            backtrack(curr.left, path)
            backtrack(curr.right, path)
            path.pop()

        backtrack(root, [])
        return root_to_leaf_paths
