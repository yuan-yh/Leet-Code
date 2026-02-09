class MyCircularDeque:
    def __init__(self, k: int):
        self.q = [0] * k
        self.size = k
        self.cnt = self.head = 0

    def insertFront(self, value: int) -> bool:
        if self.isFull(): return False
        self.head = (self.head - 1) % self.size
        self.q[self.head] = value
        self.cnt += 1
        return True

    def insertLast(self, value: int) -> bool:
        if self.isFull(): return False
        tail = (self.head + self.cnt) % self.size
        self.q[tail] = value
        self.cnt += 1
        return True

    def deleteFront(self) -> bool:
        if self.isEmpty(): return False
        self.cnt -= 1
        self.head = (self.head + 1) % self.size
        return True

    def deleteLast(self) -> bool:
        if self.isEmpty(): return False
        self.cnt -= 1
        return True

    def getFront(self) -> int:
        return -1 if self.isEmpty() else self.q[self.head]

    def getRear(self) -> int:
        tail = (self.head + self.cnt - 1) % self.size
        return -1 if self.isEmpty() else self.q[tail]

    def isEmpty(self) -> bool:
        return self.cnt == 0

    def isFull(self) -> bool:
        return self.cnt == self.size


# Your MyCircularDeque object will be instantiated and called as such:
# obj = MyCircularDeque(k)
# param_1 = obj.insertFront(value)
# param_2 = obj.insertLast(value)
# param_3 = obj.deleteFront()
# param_4 = obj.deleteLast()
# param_5 = obj.getFront()
# param_6 = obj.getRear()
# param_7 = obj.isEmpty()
# param_8 = obj.isFull()