class Solution:
    def canJump(self, nums: List[int]) -> bool:
        # Greedy: track the max jump length
        jump = 0
        for i, n in enumerate(nums):
            # 1. check if the current position accessible
            if jump < i: return False
            # 2. update the max length
            jump = max(jump, i + n)
        return True