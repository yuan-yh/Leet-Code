''' Assume the set p for plus and the set m for minus, 
sum(p) - sum(m) = target
sum(p) + sum(m) = total
->
sum(p) = (target + total) >> 1 <- fill this bag '''

class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        size = sum(nums) + target
        if size % 2 != 0 or size < 0: return 0

        size >>= 1
        dp = [1] + [0] * size

        for n in nums:
            for i in range(size, n-1, -1):
                dp[i] += dp[i - n]
        return dp[-1]