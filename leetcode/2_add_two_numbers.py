from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        # 2 -> 4 -> 3, 342
        # 6 -> 4,       46
        # Numbers don't contain leading zero, won't be ending zeros in linked list
        # linked list is not empty, at least 1 node, of unknown length

        # Return the head of a linked list which represents the sum
        # resulting LL is also in reverse order

        # Track carry over to next sum of two nodes in LL
        # Length of linked list may differ
        # For first k nodes, where k is length of smaller of two linked lists, perform normal addition per node plus track carry
        # For the suffix of longer LL remaining, we add those values through node.val * (10^idx)
        # O(n) time, O(1) space

        dummy = ListNode()
        curr_res = dummy
        carry = 0
        curr1, curr2 = l1, l2
        idx = 0
        while curr1 is not None or curr2 is not None:
            if curr1 is not None and curr2 is not None:
                digit = curr1.val + curr2.val + carry            
            elif curr1 is not None:
                digit = curr1.val + carry
            else:
                digit = curr2.val + carry

            if digit >= 10:
                carry = 1
                digit %= 10
            else:
                carry = 0
            
            res_node = ListNode(digit)
            curr_res.next = res_node
            curr_res = res_node
            idx += 1
            curr1 = curr1.next if curr1 is not None else None
            curr2 = curr2.next if curr2 is not None else None
    
        if carry == 1:
            curr_res.next = ListNode(carry)
        
        return dummy.next
