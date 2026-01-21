class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        # Key Insight: 0-1背包 -> check if we can fill the bag of size n (half)
        total = sum(nums)
        if total % 2 != 0: return False

        total >>= 1
        dp = [True] + [False] * total

        for n in nums:
            # fill backwards to avoid repeat adding
            for i in range(total, n-1, -1):
                if not dp[i]: dp[i] = dp[i-n]
        return dp[-1]