class MinStack:
    def __init__(self):
        self.minstack = [(0, inf)]  # init with (any_val, min)

    def push(self, val: int) -> None:
        self.minstack.append((val, min(val, self.minstack[-1][1])))

    def pop(self) -> None:
        self.minstack.pop()

    def top(self) -> int:
        return self.minstack[-1][0]

    def getMin(self) -> int:
        return self.minstack[-1][1]


# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()