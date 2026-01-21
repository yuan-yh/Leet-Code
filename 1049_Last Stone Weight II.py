class Solution:
    def lastStoneWeightII(self, stones: List[int]) -> int:
        # Ideal case: split into two equal piles so all smashed
        # Therefore, try to fill the bag[half + 1]
        total = sum(stones)
        size = total >> 1

        dp = [0] * (size + 1)
        for s in stones:
            for i in range(size, s-1, -1):
                dp[i] = max(dp[i], dp[i - s] + s)

        left, right = total - dp[-1], dp[-1]
        return abs(left - right)