from typing import List, Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        root_to_leaf_paths = []

        def dfs(path_sum: int, path: list[int], curr_node: Optional[TreeNode]) -> None:
            if curr_node is None:
                return

            path_sum += curr_node.val
            path.append(curr_node.val)
            # Process left child
            dfs(path_sum, path, curr_node.left)

            # Process right child
            dfs(path_sum, path, curr_node.right)

            # Process curr node
            if curr_node.left is None and curr_node.right is None and path_sum == targetSum:
                root_to_leaf_paths.append(path.copy())

            path.pop()

        dfs(0, [], root)
        return root_to_leaf_paths
