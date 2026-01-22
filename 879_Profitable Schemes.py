class Solution:
    def profitableSchemes(self, n: int, minProfit: int, group: List[int], profit: List[int]) -> int:
        """
        容斥原理: `g <= n, p >= minProfit的组合个数` == `g<=n的组合个数` 减去 `g<=n,p < minProfit的个数`
        同时满足 A 和 B = 满足A的全部 - 满足A但不满足B的
        """
        mod = 10**9 + 7

        # 1. g<=n的组合个数
        dp_g = [1] + [0] * n
        for g in group:
            for i in range(n, g-1, -1):
                dp_g[i] += dp_g[i - g]
        sum_g = sum(dp_g)   # 所有人数 ≤ n 的方案总数

        # edge case
        if minProfit == 0: return sum_g % mod
        
        # 2. g<=n,p < minProfit的个数 <- 0-1背包
        dp_m = [[0] * minProfit for _ in range(1 + n)]   # row: headcnt, col: profit
        dp_m[0][0] = 1
        for g, p in zip(group, profit):
            for r in range(n, g-1, -1):
                for c in range(minProfit-1, p-1, -1):
                    dp_m[r][c] += dp_m[r-g][c-p]
        sum_m = sum(sum(dp_m[r]) for r in range(n+1))
        
        return (sum_g - sum_m) % mod