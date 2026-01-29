from typing import Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def removeLeafNodes(self, root: Optional[TreeNode], target: int) -> Optional[TreeNode]:
        # only want to remove leaf nodes, which have the target value
        # continuously remove any new leaf nodes that form as a result which also have target value

        #    3
        #  3   3  --> return null?
        # Should we modify in-place? Do we return the new root of the tree?

        # We see an identical subproblem; essentially we return the root of the subtree that we have left
        # Base case is where root itself is a leaf -> remove or not only depends on whether it matches target

        if root is None:
            return None

        root.left = self.removeLeafNodes(root.left, target)
        root.right = self.removeLeafNodes(root.right, target)

        if self.shouldRemove(root, target):
            return None
        else:
            return root

    def shouldRemove(self, node: Optional[TreeNode], target: int) -> bool:
        if node is None:
            return False
        
        if node.left is not None or node.right is not None:
            return False
        
        # At this point, we know that it is a leaf
        return node.val == target