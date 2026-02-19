class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        slow = 0
        for n in nums:
            if n != 0:
                nums[slow] = n
                slow += 1
        for i in range(slow, len(nums)): 
            nums[i] = 0