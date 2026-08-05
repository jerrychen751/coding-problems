from typing import List, Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def printTree(self, root: Optional[TreeNode]) -> List[List[str]]:
        # DFS to get height of tree first
        # Then DFS to place nodes in their positions
        # Perform postorder traversal

        def get_height(root: Optional[TreeNode]) -> int:
            if root is None:
                return -1

            return 1 + max(get_height(root.left), get_height(root.right))

        height = get_height(root)
        # guaranteed to have at least 1 node

        m = height + 1
        n = 2 ** (height + 1) - 1
        matrix = [["" for _ in range(n)] for _ in range(m)]
        def dfs(curr: Optional[TreeNode], parent_i: int, parent_j: int, child_dir: str) -> None:
            """
            curr is current node, (parent_i, parent_j) describe position in matrix of curr's parent, child_dir is
            'L' if curr is parent's left child and 'R' if parent's right child.
            """
            if curr is None:
                return

            curr_i = parent_i + 1
            curr_j = parent_j - 2 ** (height - parent_i - 1) if child_dir == 'L' else parent_j + 2 ** (height - parent_i - 1)

            dfs(curr.left, curr_i, curr_j, 'L')
            dfs(curr.right, curr_i, curr_j, 'R')
            matrix[curr_i][curr_j] = str(curr.val)

        root_i, root_j = 0, (n - 1) // 2
        matrix[root_i][root_j] = str(root.val)
        dfs(root.left, root_i, root_j, 'L')
        dfs(root.right, root_i, root_j, 'R')
        return matrix
