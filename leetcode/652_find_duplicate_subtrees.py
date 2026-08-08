from typing import List, Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution1:
    def findDuplicateSubtrees(self, root: Optional[TreeNode]) -> List[Optional[TreeNode]]:
        # Maintain a map that maps id(node) to a numerical identifier
        # That way, two subtrees that are equal can go through this mapping to determine whether their values are equal or not
        # Two trees are determined equal if map[id(node.left)] == map[id(other.left)] and map[id(node.right)] == map[id(other.right)] and node.val == other.val

        id_to_identifier: dict[int, int] = {} # maps id(node) to a unique value
        val_to_node: dict[int, list[TreeNode]] = {}
        duplicates = []
        duplicate_ids = set() # set of values (value in id_to_identifier dict) for equal subtrees
        id_to_identifier[id(None)] = id(None)

        def find_duplicates(curr: Optional[TreeNode]) -> None:
            if curr is None:
                return

            # Postorder traversal
            find_duplicates(curr.left)
            find_duplicates(curr.right)

            # Either we've seen a node of the same value before, or we haven't
            if curr.val not in val_to_node:
                # If not seen, then we add and there's no way for this node to be a duplicate of anything we've seen so far
                val_to_node[curr.val] = [curr]
                id_to_identifier[id(curr)] = id(curr) # guaranteed uniqueness; next time we find a duplicate subtree we change their mapping from their memory address to this same id value as existing tree
            else:
                # If we've seen, then we need to test for duplicates against all unique seen nodes w/ same value
                for other in val_to_node[curr.val]:
                    if id_to_identifier[id(curr.left)] == id_to_identifier[id(other.left)] and id_to_identifier[id(curr.right)] == id_to_identifier[id(other.right)]:

                        # We've found a duplicate
                        if id_to_identifier[id(other)] not in duplicate_ids:
                            # Add only if this subtree wasn't deemed as duplicate already
                            duplicates.append(curr)

                        duplicate_ids.add(id_to_identifier[id(other)])
                        id_to_identifier[id(curr)] = id_to_identifier[id(other)]
                        break

                else:
                    val_to_node[curr.val].append(curr)
                    id_to_identifier[id(curr)] = id(curr)

        find_duplicates(root)
        return duplicates


class Solution2:
    def findDuplicateSubtrees(self, root: Optional[TreeNode]) -> List[Optional[TreeNode]]:
        # Maintain a map that maps id(node) to a numerical identifier
        # That way, two subtrees that are equal can go through this mapping to determine whether their values are equal or not
        # Two trees are determined equal if map[id(node.left)] == map[id(other.left)] and map[id(node.right)] == map[id(other.right)] and node.val == other.val

        id_to_identifier: dict[tuple[int, int, int], int] = {} # maps (val, left_id, right_id) to a unique value
        # All other nodes with same (val, left_id, right_id) will then be checked against keys of id_to_identifier
        # If in there, and id_to_identifier[(val, left_id, right_id)] is not in duplicate_ids, add to set and set as duplicate
        duplicates = []
        duplicate_ids = set() # set of values (value in id_to_identifier dict) for equal subtrees

        def find_duplicates(curr: Optional[TreeNode]) -> int:
            if curr is None:
                return id(None)

            # Postorder traversal
            left_identifier = find_duplicates(curr.left)
            right_identifier = find_duplicates(curr.right)

            curr_id = (curr.val, left_identifier, right_identifier)
            if curr_id in id_to_identifier:
                if id_to_identifier[curr_id] not in duplicate_ids:
                    duplicate_ids.add(id_to_identifier[curr_id])
                    duplicates.append(curr)
            else:
                id_to_identifier[curr_id] = id(curr)

            return id_to_identifier[curr_id]

        find_duplicates(root)
        return duplicates
