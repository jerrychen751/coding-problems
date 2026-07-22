from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def smallestFromLeaf(self, root: Optional[TreeNode]) -> str:
        # Node value is an int from 0..25 representing 26 letters in alphabet
        # Return the smallest string that starts at a leaf and ends at the root
        # Considering dfs approach using preorder traversal (parent first then left/right children)
        # Need to track curr node, path up to curr node, and globally smallest string lexicographically

        # Originally considered tracking string, but appending string forms new string and is inefficient each time compared to appending to a list and iterating through once in reversed order using custom function
        smallest_path = [[float('inf')]]

        def dfs(curr: Optional[TreeNode], path: list[int]) -> None:
            if curr is None:
                return

            path.append(curr.val)
            if curr.left is None and curr.right is None:
                candidate = path[::-1]
                if candidate < smallest_path[0]:
                    smallest_path[0] = candidate

            dfs(curr.left, path)
            dfs(curr.right, path)
            path.pop()

        dfs(root, [])
        res = "".join([chr(97 + v) for v in smallest_path[0]])
        return res
