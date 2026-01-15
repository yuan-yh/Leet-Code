
# Greedy: jump a new step to the next furthest landing position when infeasible
class Solution:
    def jump(self, nums: List[int]) -> int:
        step, curLand, nextLand = 0, 0, nums[0]

        for i, n in enumerate(nums):
            # case: within cur jump -> update next landing
            # case: outside cur jump -> new jump to next landing then update next landing
            if i > curLand:
                curLand = nextLand
                step += 1
            nextLand = max(nextLand, i + n)
        
        return step