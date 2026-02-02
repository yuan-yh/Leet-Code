class MovingAverage:

    def __init__(self, size: int):
        self.size = size
        self.record = deque()
        self.total = 0

    def next(self, val: int) -> float:
        if len(self.record) == self.size:
            expire = self.record.popleft()
            self.total -= expire
        
        self.record.append(val)
        self.total += val

        return self.total / len(self.record)


# Your MovingAverage object will be instantiated and called as such:
# obj = MovingAverage(size)
# param_1 = obj.next(val)