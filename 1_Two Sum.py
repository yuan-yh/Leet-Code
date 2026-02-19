class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        record = {}

        for i, n in enumerate(nums):
            if n in record: return [record[n], i]
            record[target - n] = i
        return [-1, -1]