from __future__ import annotations


# Initialize with some capacity
# Support get and put methods, running in O(1) average time complexity
# Cache based on keys, retrieve values, don't cache all keys/values but rather a limited capacity
# When capacity is full and we're adding a new element, discard the oldest key-value pair from cache

# Need O(1) access and placement -> hash map
# However, we also need an idea of recency, and easily removing oldest / adding newest: doubly-linked list or queue
# Queue doesn't work well because if we have a mid-aged key-value pair that becomes most recent it takes O(n)

class Node:
    def __init__(self, key: int, val: int, prev: Node | None = None, next: Node | None = None) -> None:
        self.key = key
        self.val = val
        self.prev = prev
        self.next = next

class LRUCache:

    def __init__(self, capacity: int):
        self.hash_map: dict[int, Node] = {}
        self.head: Node | None = None # most recently accessed
        self.tail: Node | None = None # least recently accessed
        self.capacity = capacity
        self.size = 0

    def get(self, key: int) -> int:
        if key not in self.hash_map:
            return -1
        
        node = self.update(key)
        return node.val

    def put(self, key: int, value: int) -> None:
        # Two scenarios: either it's already there and we update value + move to most recently accessed
        # or it's new and we add it to LRU cache, evicting if needed
        if key in self.hash_map:
            node = self.update(key)
            node.val = value
        else:
            if self.size == self.capacity:
                # Evict LRU node: remove tail and also remove that key from self.hash_map
                # Can essentially replace key + value
                # Remove tail
                old_tail = self.tail
                new_tail = self.tail.prev
                if new_tail is None:
                    self.head = None
                    self.tail = None
                else:
                    new_tail.next = None
                    self.tail = new_tail
                del self.hash_map[old_tail.key]
                self.size -= 1

            # Add newly created node as head of DLL + add to hash map
            new_node = Node(key, value, None, self.head)
            if self.head is None:
                self.head = new_node
                self.tail = new_node
            else:
                self.head.prev = new_node
            self.head = new_node
            self.hash_map[key] = new_node
            self.size += 1
    
    def update(self, key: int) -> Node:
        # Set a node as recently accessed by moving it to front of DLL
        node = self.hash_map[key]

        if node is self.head:
            return node
        
        # Remove node from DLL
        if node.prev is not None:
            node.prev.next = node.next
        if node.next is not None:
            node.next.prev = node.prev
        else: # edge case: node is the tail -> update tail
            self.tail = node.prev

        node.prev = None
        node.next = self.head
        self.head.prev = node
        self.head = node
        return node

# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
