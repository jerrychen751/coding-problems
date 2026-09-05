'''
stack + monotonic stack
stack push/pop/top operates normally
maintain an additional monotonicaly decreasing stack; least element at left end, largest at right end
Say we have [2, 3, 5, 1] pushed in that order
then monotonic stack build step would be [(2, 0), (1, 3)]
when popping we check against stack[-1][1] index if at that then we remove
'''

class MinStack:
    def __init__(self):
        self.stack = []
        self.decreasing_stack = [] # stores (num, idx)

    def push(self, value: int) -> None:
        idx = len(self.stack) # location of value within stack
        self.stack.append(value)
        if not self.decreasing_stack:
            self.decreasing_stack.append((value, idx))
        else:
            if value < self.decreasing_stack[-1][0]:
                self.decreasing_stack.append((value, idx))

    def pop(self) -> None:
        idx = len(self.stack) - 1 # idx of element in stack to be popped
        self.stack.pop()
        if self.decreasing_stack and self.decreasing_stack[-1][1] == idx:
            self.decreasing_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.decreasing_stack[-1][0]

# Your MinStack object will be instantiated and called as such:

# obj = MinStack()

# obj.push(value)

# obj.pop()

# param_3 = obj.top()

# param_4 = obj.getMin()
