class MinStack:
    # Keep tracking the valid min-val at the cur stack element
    def __init__(self):
        self.minStack = [(0, inf)]  # init with (any_val, min)

    def push(self, val: int) -> None:
        self.minStack.append((val, min(val, self.minStack[-1][1])))

    def pop(self) -> None:
        self.minStack.pop()

    def top(self) -> int:
        return self.minStack[-1][0]

    def getMin(self) -> int:
        return self.minStack[-1][1]
        


# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()