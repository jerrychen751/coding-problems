from typing import Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head:
            return None

        # Floyd's cycle detection
        slow = fast = head
        has_cycle = False
        while fast.next and fast.next.next:
            prev = slow
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                has_cycle = True
                break

        if not has_cycle:
            return None

        # Let mu = acyclical prefix length, lambda = cycle length
        # n = mu + lambda is length of linked list
        # Let t be the number of iterations of the while loop, which is also the index of the linked list which slow is on
        # Let s be slow's offset from cycle entry (index within cycle), f for fast
        # s = (t - mu) % lambda
        # f = (2t - mu) % lambda
        # Condition for s == f (first meeting) is t - mu = 2t - mu (mod lambda), or t = 0 (mod lambda)
        # Since this offset is after traversing acyclical prefix, t < mu + lambda = n, thus O(n) traversal for cycle detection

        # Now we want to determine the value of mu
        # i.e., we want the entrypoint to the cycle
        # At this point, we know t = k * lambda

        # Then, s = f = -mu (mod lambda)
        # If slow is reset from (mu + s) to 0, it is guaranteed to meet fast at the entrypoint of the cycle
        # Because fast = -mu (mod lambda) so f = 0 (mod lambda) after mu steps, landing at the entrypoint of the cycle
        # If both slow and fast traverse at the same pace, they'll eventually meet at the entrypoint
        slow = head
        while slow != fast:
            slow = slow.next
            fast = fast.next

        return slow
