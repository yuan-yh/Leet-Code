class Solution:
    def profitableSchemes(self, n: int, minProfit: int, group: List[int], profit: List[int]) -> int:
        """容斥原理: 同時滿足A和B的數量 = 滿足A的數量 - 滿足A但不滿足B的數量
        """
        """
        容斥原理: `g <= n, p >= minProfit的组合个数` == `g<=n的组合个数` 减去 `g<=n,p < minProfit的个数`
        同时满足 A 和 B = 满足A的全部 - 满足A但不满足B的
        """
        mod = 10**9 + 7
        # 1. scheme cnt of headcnt <= n
        # 1. g<=n的组合个数
        dp1 = [1] + [0] * n
        for g in group:
            for i in range(n, g-1, -1):
                dp1[i] += dp1[i - g]
        # short-cut: if minProfit == 0
        if minProfit == 0: return sum(dp1)%mod

        # 2. scheme cnt of headcnt <= n & profit < minProfit
        # 2. g<=n,p < minProfit的个数 <- 0-1背包
        dp2 = [[0] * minProfit for _ in range(n+1)]    # row: headcnt, col: profit
        dp2[0][0] = 1

        for g, p in zip(group, profit): 
            for r in range(n, g-1, -1):
                for c in range(minProfit-1, p-1, -1):
                    dp2[r][c] += dp2[r-g][c-p]

        return (sum(dp1) - sum(sum(dp2[i]) for i in range(n+1))) % mod