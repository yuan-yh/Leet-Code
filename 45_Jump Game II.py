
# Greedy: jump a new step to the next furthest landing position when infeasible
class Solution:
    def jump(self, nums: List[int]) -> int:
        step, cur, land, target = 0, 0, nums[0], len(nums) - 1

        for i, jump in enumerate(nums):
            if cur < i:
                step += 1
                cur = land
            land = max(land, i + jump)
            if cur >= target: break
        return step