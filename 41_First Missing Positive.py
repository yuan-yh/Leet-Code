class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        """res in range [1, len(nums) + 1]
        So swap nums[i] to idx nums[i]-1, then look for the first i such that nums[i] != i+1
        """
        length = len(nums)
        # 1. swap
        for i in range(length):
            while 0 < nums[i] <= length and nums[i] != i+1 and nums[nums[i]-1] != nums[i]:
                tmp = nums[nums[i] - 1]
                nums[nums[i] - 1] = nums[i]
                nums[i] = tmp
        # 2. find the first i != nums[i]-1
        for i, n in enumerate(nums):
            if n != i+1: return i+1
        return length + 1