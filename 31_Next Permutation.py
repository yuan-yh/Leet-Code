class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        if len(nums) <= 1: return
        # 1. find the latest i such that nums[i] < nums[i+1]
        i = len(nums) - 2
        while i >= 0 and nums[i] >= nums[i+1]: i -= 1
        # 2. find the smallest j in nums[i+1:] such that nums[i] < nums[j], then swap
        if i >= 0:
            j = len(nums) - 1
            while i < j and nums[i] >= nums[j]: j -= 1
            nums[i], nums[j] = nums[j], nums[i]
        # 3. Now nums[i+1:] in DESC, reverse
        i, j = i + 1, len(nums) - 1
        while i < j:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1
            j -= 1