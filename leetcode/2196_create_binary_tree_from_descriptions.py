from typing import List, Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def createBinaryTree(self, descriptions: List[List[int]]) -> Optional[TreeNode]:
        # Process descriptions in order
        # Create hash map to store num -> TreeNode mapping
        # When parent is in hash map, obtain reference to parent and use that
        # If child is in hash map, then use that. Otherwise create a new TreeNode
        # When we come across a description, we can immediately create the parent node and child node and link the two together
        # Then we can add both the parent and child to a hash map, where the key is number and value is reference to created TreeNode
        if len(descriptions) == 0:
            return None

        mapping = {}
        children = set()
        for description in descriptions:
            parent, child, is_left = description
            children.add(child)

            child_node = mapping.get(child, TreeNode(child))
            parent_node = mapping.get(parent, TreeNode(parent))
            if is_left == 1:
                parent_node.left = child_node
            else:
                parent_node.right = child_node
            
            mapping[child] = child_node
            mapping[parent] = parent_node
        
        for node_val in mapping:
            if node_val not in children:
                return mapping[node_val]