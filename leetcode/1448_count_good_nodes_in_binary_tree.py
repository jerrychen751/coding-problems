from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val: int = val
        self.left: Optional[TreeNode] = left
        self.right: Optional[TreeNode] = right


class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        # As we traverse through the tree, we need to perform preorder traversal
        # Visit the parent of each node first, starting from root
        
        # Return the number of good nodes in a tree with root = node
        def dfs(node: Optional[TreeNode], max_val: int) -> int:
            if node is None:
                return 0
            
            if max_val <= node.val:
                max_val = node.val
                return 1 + dfs(node.left, max_val) + dfs(node.right, max_val)
            
            return dfs(node.left, max_val) + dfs(node.right, max_val)
        
        return dfs(root, root.val - 1)