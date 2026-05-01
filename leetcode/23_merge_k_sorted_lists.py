from typing import List, Optional
import heapq

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Heap:
    def __init__(self, arr: List[Optional[ListNode]]) -> None:
        self.min_heap = [n for n in arr if n is not None]
        self.heapify()

    def is_empty(self) -> bool:
        return len(self.min_heap) == 0

    def pop(self) -> Optional[ListNode]:
        if self.is_empty():
            return None
        if len(self.min_heap) == 1:
            return self.min_heap.pop()

        smallest = self.min_heap[0]
        self.min_heap[0] = self.min_heap.pop()
        self._sift_down(0)
        return smallest

    def push(self, node: Optional[ListNode]) -> None:
        if node is None:
            return

        self.min_heap.append(node)
        self._sift_up(len(self.min_heap) - 1)

    def heapify(self) -> None:
        for i in range(len(self.min_heap) // 2 - 1, -1, -1):
            self._sift_down(i)

    def _sift_up(self, i: int) -> None:
        while i > 0:
            parent = (i - 1) // 2
            if self.min_heap[parent].val <= self.min_heap[i].val:
                break
            self.min_heap[i], self.min_heap[parent] = self.min_heap[parent], self.min_heap[i]
            i = parent

    def _sift_down(self, i: int) -> None:
        n = len(self.min_heap)
        while True:
            left = 2 * i + 1
            right = 2 * i + 2
            min_idx = i
            if left >= n:
                break

            if left < n and self.min_heap[left].val < self.min_heap[min_idx].val:
                min_idx = left
            if right < n and self.min_heap[right].val < self.min_heap[min_idx].val:
                min_idx = right
            if min_idx == i:
                return
            self.min_heap[min_idx], self.min_heap[i] = self.min_heap[i], self.min_heap[min_idx]
            i = min_idx

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if len(lists) == 0:
            return None

        h = Heap(lists)
        dummy = ListNode(0, None)
        curr = dummy
        while not h.is_empty():
            new_node = h.pop()
            h.push(new_node.next) # no-op if next is None
            curr.next = new_node
            curr = curr.next

        return dummy.next
