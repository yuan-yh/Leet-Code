class FirstUnique:
    # Lazy Deletion
    def __init__(self, nums: List[int]):
        self.q = deque(nums)
        self.cnt = Counter(nums)

    def showFirstUnique(self) -> int:
        while self.q and self.cnt[self.q[0]] > 1: self.q.popleft()
        return self.q[0] if self.q else -1

    def add(self, value: int) -> None:
        if self.cnt[value] == 0: self.q.append(value)
        self.cnt[value] += 1


# Your FirstUnique object will be instantiated and called as such:
# obj = FirstUnique(nums)
# param_1 = obj.showFirstUnique()
# obj.add(value)