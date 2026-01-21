# Greedy
class Solution:
    def canJump(self, nums: List[int]) -> bool:
        land = nums[0]
        
        for i, jump in enumerate(nums):
            if land < i: return False
            land = max(land, i + jump)
        return True