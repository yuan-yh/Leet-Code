// 时间复杂度：O(n⋅amount)，其中 n 为 coins 的长度。
// 空间复杂度：O(amount)。

class Solution {
    public int coinChange(int[] coins, int amount) {
        // 完全背包: each items can be added multiple times

        // edge case: 0
        if (amount == 0) return 0;

        int[] dp = new int[amount+1];
        // init
        for (int i = 1; i <= amount; i++) dp[i] = Integer.MAX_VALUE / 2;

        // process
        for (int c : coins) {
            for (int i = c; i <= amount; i++) {
                dp[i] = Math.min(dp[i], dp[i-c]+1);
            }
        }

        return (dp[amount] < Integer.MAX_VALUE / 2 ? dp[amount] : -1);
    }
}