from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def longestZigZag(self, root: Optional[TreeNode]) -> int:
        # We want to return number of edges in the longest zig-zag path from any node to any node in the tree
        # Notice that it doesn't necessarily have to start from root or end on leaf

        # special cases:
        # if node is alone, should return 0 dist
        # if node is null, should return -1 dist

        # recursive nature of the problem
        # longest zig-zag at some node is max(longestZigZag(left), longestZigZag(right)) + 1
        # as long as dir is opposite

        # we discard the shorter length because there is only one possible parent to move up for
        # in this case, we can be greedy and just keep the larger of the two to continue using

        # we can use some form of postorder traversal, because the answer at any node
        # is built from its children

        # Let dir == -1 denote left and dir == 1 denote right
        # Returns (dist, dir) where dir is the direction of the longest zigzag dist
        # For a node that is alone, we can return dir of 0 to indicate it can be either
        
        # dist = number of nodes visited in path - 1
        # if root is None -> return -1
        # if root is a leaf -> return 0
        # dfs(node) can return two values; longest zigzag going left and longest zigzag going right
        # caller can make decision for which to use, because only the caller has sense of direction
        # finally, when we get left, right = dfs(root) -> return max(left, right)
        
        self.max_dist = 0

        def dfs(node: Optional[TreeNode]) -> tuple[int, int]: # (longest left zigzag, longest right zigzag)
            if node is None:
                return -1, -1
            
            left_l, left_r = dfs(node.left) # longest path moving left/right from left child
            right_l, right_r = dfs(node.right)

            curr_left = left_r + 1
            curr_right = right_l + 1
            self.max_dist = max(self.max_dist, curr_left, curr_right)
            return curr_left, curr_right

        dfs(root)
        return self.max_dist