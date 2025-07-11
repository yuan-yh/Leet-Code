// 时间复杂度：O(n⋅amount)，其中 n 为 coins 的长度。
// 空间复杂度：O(amount)。

class Solution {
    public int change(int amount, int[] coins) {
        // 完全背包
        int[] dp = new int[amount + 1];
        dp[0] = 1;

        for (int c : coins) {
            for (int i = c; i <= amount; i++) {
                dp[i] += dp[i - c];
            }
        }
        return dp[amount];
    }
}