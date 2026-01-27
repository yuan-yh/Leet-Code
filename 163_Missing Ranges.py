class Solution:
    def findMissingRanges(self, nums: List[int], lower: int, upper: int) -> List[List[int]]:
        """Missing Range: [start, nums[i]) or (nusm[i], nums[i+1]) or (nums[-1], end]"""
        if len(nums) == 0: return [[lower, upper]]

        res = []
        for i, n in enumerate(nums):
            if i == 0 and n > lower: res.append([lower, n-1])
            
            if i > 0 and n > nums[i-1]+1: res.append([nums[i-1]+1, n-1])
            
            if i == len(nums)-1 and n < upper: res.append([n+1, upper])
        return res