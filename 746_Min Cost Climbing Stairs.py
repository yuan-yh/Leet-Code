class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        dp = [0, 0]
        for c in cost:
            tmp = dp[0] + c
            dp[0], dp[1] = min(dp[1], tmp), tmp
        return dp[0]