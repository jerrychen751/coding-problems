from typing import Optional

# Definition for a Node.
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random


class Solution1:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        # Obtain a deep copy of a linked list, where this linked list's nodes
        # have not only a next pointer to another node, but also a random pointer
        # New copy's pointers should point to new nodes, not original nodes

        # Since we don't know where the random pointer points, we need at least 2 passes
        # The first time we traverse through the original list, we create each node's copy
        # and form their next pointer, as well as create a mapping from an original node to its copy

        # in our second pass, we go through the original list and look at the random ptr
        # We look at a node's random ptr (some other original node), then set map[node].random = map[node.random]

        if head is None:
            return None

        hmap = {}
        curr = head
        prev_cpy = None
        while curr is not None:
            curr_cpy = Node(curr.val, None, None)
            if prev_cpy is not None:
                prev_cpy.next = curr_cpy
            prev_cpy = curr_cpy
            hmap[id(curr)] = curr_cpy

            curr = curr.next

        curr = head
        while curr is not None:
            hmap[id(curr)].random = hmap[id(curr.random)] if curr.random is not None else None
            curr = curr.next

        return hmap[id(head)]


class Solution2:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        # Is there a way to avoid O(n) space
        # We need a way to traverse from the original node to the next node in the original list,
        # but also from the original node to copy of original's random node i.e. hmap[id(curr.random)]
        # A > A' > B > B' > C > C'...

        # Use 1 pass to create copy and insert it right behind original node
        # Use another pass to set random ptrs for each node copy; cpy.random = orig.random.next
        # Use final pass to detach copied linked list from original linked list

        if head is None:
            return None

        # Build copy
        curr = head
        nxt = None
        while curr is not None:
            nxt = curr.next
            curr.next = Node(curr.val, nxt, None)
            curr = nxt

        # Set random ptrs
        curr = head
        while curr is not None:
            if curr.random is not None: # only triggers for original nodes with .random != None
                curr.next.random = curr.random.next
            curr = curr.next.next

        # Detach copied linked list
        new_head = None # head of deep copy
        tail = None # last node in deep copy linked list; used to append new nodes
        curr = head
        while curr is not None:
            curr_cpy = curr.next
            if new_head is None:
                new_head = curr_cpy
                tail = curr_cpy
            else:
                tail.next = curr_cpy
                tail = tail.next

            curr.next = curr_cpy.next
            curr = curr.next

        return new_head
