from typing import Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # Traverse linked list and push each element to a heap as (val, node)
        # Pop the heap and adjust next pointers one at a time now that we have references to each node
        # O(nlogn) time, O(n) space

        # Better idea: take ceil(log(n)) passes mirroring bottom-up structure of merge sort
        # Say we have 4 -> 2 -> 1 -> 3
        # Start with res = []
        # Break up into 4, 2, 1 -> 3 (we have references to 4, 2, and 1)
        # tail.next = min(head1, head2)
        # res = [2, 4], curr = 1
        # head1 = 1, head2 = 3

        size = 1

        # Count length of the list
        n = 0
        curr = head
        while curr is not None:
            n += 1
            curr = curr.next

        if n <= 1:
            return head

        dummy = ListNode(0, head)
        tail = dummy # Point to last node in the semi-sorted result of a merge level which is finalized

        while size < n:
            # Obtain splits, where each split is guaranteed to be in sorted order
            # We track the heads of both splits, and then add onto the linked list using tail.next
            curr = dummy.next # at beginning of each merge layer we start at beginning
            tail = dummy
            while curr is not None:
                left = curr
                right, left_last = self._split(left, size)
                curr, right_last = self._split(right, size) # curr now points to the node after both splits; left... right... curr

                # At this point, left and right are heads of sorted linked lists
                # We merge two sorted linked lists
                while left is not None and right is not None:
                    if left.val <= right.val:
                        tail.next = left
                        left = left.next
                    else:
                        tail.next = right
                        right = right.next
                    tail = tail.next
                if left is not None:
                    tail.next = left
                    tail = left_last
                if right is not None:
                    tail.next = right
                    tail = right_last

            size *= 2 # Size increases for next merge layer

        return dummy.next

    def _split(self, curr: Optional[ListNode], size: int) -> tuple[Optional[ListNode], ListNode]:
        """Takes size number of nodes, starting from curr, and returns a reference to the node after this subset of nodes. The last node's next pointer is set to None so that we know when it is the end of a particular piece."""
        if curr is None:
            return None, None

        ct = 1
        while curr.next is not None and ct < size:
            ct += 1
            curr = curr.next

        nxt = curr.next
        curr.next = None
        return nxt, curr
