class MyQueue:
    # append into stack_out, pop from stack_out
    def __init__(self):
        self.sin = []
        self.sout = []

    def push(self, x: int) -> None:
        self.sin.append(x)

    def pop(self) -> int:
        if not self.sout:
            while self.sin: self.sout.append(self.sin.pop())
        return self.sout.pop()

    def peek(self) -> int:
        target = self.pop()
        self.sout.append(target)
        return target

    def empty(self) -> bool:
        return len(self.sin) == 0 and len(self.sout) == 0


# Your MyQueue object will be instantiated and called as such:
# obj = MyQueue()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.peek()
# param_4 = obj.empty()