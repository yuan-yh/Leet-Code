class RandomizedSet:
    # insert/remove O(1): track w/ hashset or dictionary
    # random O(1): fetch from array index
    def __init__(self):
        self.record = {}   # val:idx
        self.nums = []

    def insert(self, val: int) -> bool:
        if val in self.record: return False
        self.record[val] = len(self.nums)
        self.nums.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.record: return False
        # swap with the tail element, then update & pop tail
        tail = self.nums[-1]
        idx = self.record[val]

        self.nums[idx] = tail
        self.record[tail] = idx

        del self.record[val]
        self.nums.pop()
        return True

    def getRandom(self) -> int:
        idx = random.randint(0, len(self.nums) - 1)
        return self.nums[idx]


# Your RandomizedSet object will be instantiated and called as such:
# obj = RandomizedSet()
# param_1 = obj.insert(val)
# param_2 = obj.remove(val)
# param_3 = obj.getRandom()