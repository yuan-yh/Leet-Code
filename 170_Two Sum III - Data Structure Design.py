class TwoSum:
    # Method 1: track through digit w/ its count
    def __init__(self):
        self.record = {}

    def add(self, number: int) -> None:
        if number not in self.record: self.record[number] = 0
        self.record[number] += 1

    def find(self, value: int) -> bool:
        for n, cnt in self.record.items():
            target = value - n
            if target not in self.record: continue
            if target == n and cnt >= 2: return True
            if target != n and target in self.record: return True
        return False
    
    # # Method 2: maintain a sorted array then 2-ptr search
    # def __init__(self):
    #     self.nums = []

    # def add(self, number: int) -> None:
    #     self.nums.append(number)

    # def find(self, value: int) -> bool:
    #     self.nums.sort()
    #     l, r = 0, len(self.nums) - 1
    #     n = self.nums
    #     while l < r:
    #         if self.nums[l] + self.nums[r] < value: l += 1
    #         elif self.nums[l] + self.nums[r] > value: r -= 1
    #         else: return True
    #     return False

# Your TwoSum object will be instantiated and called as such:
# obj = TwoSum()
# obj.add(number)
# param_2 = obj.find(value)