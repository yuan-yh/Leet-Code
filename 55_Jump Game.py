# Greedy
class Solution:
    def canJump(self, nums: List[int]) -> bool:
        if len(nums) == 0: return True

        target, land = len(nums) - 1, nums[0]

        for i in range(1, len(nums)):
            if land < i: return False
            land = max(land, i + nums[i])
        return True