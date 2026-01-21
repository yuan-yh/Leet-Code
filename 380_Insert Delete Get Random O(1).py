class RandomizedSet:

    def __init__(self):
        self.nums = []
        self.record = defaultdict()     # key: nums[i], val: i

    def insert(self, val: int) -> bool:
        # insert & True if not exist
        if val in self.record: return False

        self.record[val] = len(self.nums)
        self.nums.append(val)
        return True

    def remove(self, val: int) -> bool:
        # remove & True if exist 
        # O(1) -> remove from tail: pop() -> swap val w/ tail
        if val not in self.record: return False

        idx, tail = self.record[val], self.nums[-1]
        self.nums[idx] = tail
        self.record[tail] = idx

        del self.record[val]
        self.nums.pop()
        return True

    def getRandom(self) -> int:
        return choice(self.nums)


# Your RandomizedSet object will be instantiated and called as such:
# obj = RandomizedSet()
# param_1 = obj.insert(val)
# param_2 = obj.remove(val)
# param_3 = obj.getRandom()