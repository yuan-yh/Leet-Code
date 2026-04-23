class MinStack:
    # getMin O(1): push (val, cur_min) together
    def __init__(self):
        self.record = []

    def push(self, val: int) -> None:
        self.record.append((val, min(val, self.record[-1][1] if self.record else inf)))

    def pop(self) -> None:
        self.record.pop()

    def top(self) -> int:
        return self.record[-1][0]

    def getMin(self) -> int:
        return self.record[-1][1]


# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()