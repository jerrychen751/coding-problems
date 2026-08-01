from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def str2tree(self, s: str) -> Optional[TreeNode]:
        # Build a binary tree from string, where pattern is root_val(left_subtree)(right_subtree)
        # And left_subtree and right_subtree are similarly constructed
        # Recursion/DFS; preorder traversal

        n = len(s)

        def construct(idx: int) -> tuple[int, Optional[TreeNode]]:
            if idx >= n:
                return idx, None

            start = idx
            while idx < n and (s[idx].isdigit() or s[idx] == '-'):
                idx += 1
            root_val = int(s[start:idx])
            root = TreeNode(root_val)

            # idx is now past the root val in the string
            # process the left subtree group
            if idx < n and s[idx] == '(':
                idx += 1
                if idx < n and s[idx] == ')':
                    idx += 1
                else:
                    idx, root.left = construct(idx)
                    # after this call idx is guaranteed to land on ')'
                    # The ')' which is wrapping the node itself denoting it as some subtree
                    idx += 1 # consume ')'

            # process the right subtree group, if exists
            if idx < n and s[idx] == '(':
                idx += 1
                # empty right subtree
                if idx < n and s[idx] == ')':
                    idx += 1
                else:
                    idx, root.right = construct(idx)
                    idx += 1

            return idx, root

        _, root = construct(0)
        return root
