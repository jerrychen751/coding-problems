from collections import deque


# Definition for a Node.
class Node:
    def __init__(self, val: int = 0, left: 'Node' = None, right: 'Node' = None, next: 'Node' = None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next


class Solution1:
    def connect(self, root: 'Node') -> 'Node':
        # BFS level-order traversal with a queue
        # When we popleft from queue, set popped node's next as queue[0] if len(queue > 0) else set
        # popped node's next as None (already done for us by default)
        if not root:
            return root

        queue = deque([root])
        while len(queue) > 0:
            for _ in range(len(queue) - 1):
                curr = queue.popleft()
                curr.next = queue[0]

                if curr.left is not None:
                    queue.append(curr.left)
                if curr.right is not None:
                    queue.append(curr.right)

            # Process last node in the level
            last = queue.popleft()
            if last.left is not None:
                queue.append(last.left)
            if last.right is not None:
                queue.append(last.right)

        return root


class Solution2:
    def connect(self, root: 'Node') -> 'Node':
        # BFS level-order traversal with a queue
        # When we popleft from queue, set popped node's next as queue[0] if len(queue > 0) else set
        # popped node's next as None (already done for us by default)

        # We aim to use constant extra space
        # When traversing a layer, keep track of curr (curr node on curr level)
        # next_head (head of next level)
        # and next_prev (next_prev.next is set to curr's child)
        # when we are moving across a layer, we set up the next pointers for the next layer so we can traverse the next layer like a linked list and do the same for the layer below that, and so on
        if not root:
            return root

        curr = root
        next_head = None
        next_prev = None
        while curr is not None:
            if curr.left is not None:
                if next_prev is not None:
                    next_prev.next = curr.left
                else:
                    next_head = curr.left
                next_prev = curr.left
            if curr.right is not None:
                if next_prev is not None:
                    next_prev.next = curr.right
                else:
                    next_head = curr.right
                next_prev = curr.right

            if curr.next is not None:
                curr = curr.next
            else:
                curr = next_head
                next_head = None
                next_prev = None

        return root
