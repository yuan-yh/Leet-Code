class MyCircularQueue:
    def __init__(self, k: int):
        self.q = [0] * k
        self.head = 0
        self.cnt = 0
        self.size = k

    def enQueue(self, value: int) -> bool:
        if self.isFull(): return False
        nextp = (self.head + self.cnt) % self.size
        self.q[nextp] = value
        self.cnt += 1
        return True

    def deQueue(self) -> bool:
        if self.isEmpty(): return False
        self.head = (self.head + 1) % self.size
        self.cnt -= 1
        return True

    def Front(self) -> int:
        return -1 if self.isEmpty() else self.q[self.head]

    def Rear(self) -> int:
        tail = (self.head + self.cnt - 1) % self.size
        return -1 if self.isEmpty() else self.q[tail]

    def isEmpty(self) -> bool:
        return self.cnt == 0

    def isFull(self) -> bool:
        return self.cnt == self.size


# Your MyCircularQueue object will be instantiated and called as such:
# obj = MyCircularQueue(k)
# param_1 = obj.enQueue(value)
# param_2 = obj.deQueue()
# param_3 = obj.Front()
# param_4 = obj.Rear()
# param_5 = obj.isEmpty()
# param_6 = obj.isFull()