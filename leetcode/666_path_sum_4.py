from typing import List


class Solution:
    def pathSum(self, nums: List[int]) -> int:
        # Integers are represented as abc (3-digit int)
        # a = depth of node, where depth starts at 1
        # b = position within its level where a level contains up to 2^(a-1) nodes, 1-indexed position
        # c = value of the node, between 0..9

        # Return sum of all paths from root to leaves
        # Ascending order means basically level-order traversal, first by depth, then by position within level, finally by value

        # Track sum from root to curr node for each node on a particular level
        # In the end iterate through dictionary of node: path_sum and add to total count if node is a leaf
        non_leaf_nodes = set()
        path_sums = {} # maps (depth, pos) to path sum from root to that node
        for num in nums:
            val = num % 10
            pos = (num // 10) % 10
            depth = num // 100

            parent_pos = (pos + 1) // 2
            parent_depth = depth - 1
            # Either is root or parent is already in path_sums
            if depth == 1:
                path_sums[(depth, pos)] = val
            else:
                path_sums[(depth, pos)] = path_sums[(parent_depth, parent_pos)] + val
                non_leaf_nodes.add((parent_depth, parent_pos))

        return sum(path_sum for node, path_sum in path_sums.items() if node not in non_leaf_nodes)
