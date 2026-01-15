class Solution:
    def findLengthOfLCIS(self, nums: List[int]) -> int:
        if len(nums) <= 1: return len(nums)
        l = res = 0
        for r in range(1, len(nums)):
            if nums[r] <= nums[r-1]: l = r
            res = max(res, r - l + 1)
        return res