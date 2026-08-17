from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def getDirections(self, root: Optional[TreeNode], startValue: int, destValue: int) -> str:
        # Find the lowest common ancestor -> that will be shortest path
        # Postorder traversal so we can be sure of presence of source/dest targets in left/right subtrees
        # when processing a potential lowest common ancestor

        '''
        node vals 1..n
        startValue, destValue
        L, R, U

        guaranteed to be present
        not same value / same node
        from start to dest direction sequence

        share common ancestor (ancestor may be one of the nodes)
        LCA guarantees shortest path
        postorder traversal
        num edges from startValue to LCA is number of "U" in the path

        state?
        path from curr node to start, path from curr node to dest
        LL, RL
        first discard common prefix of paths
        turn start node path into "U"
        return start_path + dest_path

        start_found = False
        dest_found = True
        start_path = []
        dest_path = []
        def dfs(node: Optional[TreeNode], path: list[str]) -> None:
            if not node return
            if start and dest found return
            if node is start:
                set start_found
                set start_path to path
                if dest found return
            if node is end:
                set end_found
                set end_path to path
                if start found return

            path.append("L")
            dfs(node.left, path)
            path.pop()
            path.append("R")
            dfs(node.right, path)
            path.pop()

        call dfs
        remove common prefix of start_path and dest_path
        return "U" * len(start_path) + dest_path
        '''
        start_found = False
        dest_found = False
        start_path = []
        dest_path = []
        path = []
        stack = [(root, "", False)]
        while stack:
            node, direction, is_exit = stack.pop()
            if node is None:
                continue
            if is_exit:
                if direction:
                    path.pop()
                continue

            if direction:
                path.append(direction)

            if node.val == startValue:
                start_found = True
                start_path.extend(path)
                if dest_found:
                    break
            if node.val == destValue:
                dest_found = True
                dest_path.extend(path)
                if start_found:
                    break

            stack.append((node, direction, True))
            stack.append((node.right, "R", False))
            stack.append((node.left, "L", False))

        idx = 0
        while idx < min(len(start_path), len(dest_path)):
            if start_path[idx] != dest_path[idx]:
                break

            idx += 1

        return "U" * (len(start_path) - idx) + "".join(dest_path[idx:])
