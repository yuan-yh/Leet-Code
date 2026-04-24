class MyStack:
    # use queue cycle_loop to simulate stack
    def __init__(self):
        self.q = []

    def push(self, x: int) -> None:
        self.q.append(x)

    def pop(self) -> int:
        length = len(self.q)
        for _ in range(length - 1):
            self.push(self.q.pop(0))
        return self.q.pop(0)

    def top(self) -> int:
        target = self.pop()
        self.push(target)
        return target

    def empty(self) -> bool:
        return len(self.q) == 0


# Your MyStack object will be instantiated and called as such:
# obj = MyStack()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.top()
# param_4 = obj.empty()