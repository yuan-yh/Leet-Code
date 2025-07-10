// 时间复杂度：O(nm)，其中 n 为 nums 的长度，m 为 nums 的元素和减去 ∣target∣。
// 空间复杂度：O(m)

class Solution {
    public int findTargetSumWays(int[] nums, int target) {
        // Method 1 (slow): binary tree - each branch is eith + or -
        // Method 2: 0-1背包 (DP)
        // sum of all selected positive nums[i] = p
        // the absolute value for sum of all selected negative nums[i] = q
        // p + q = complete array sum s
        // p - q = target t
        // Therefore, p = (t + s) / 2 => bag size = p => how many ways to fill the backpack

        int sum = 0;
        for (int n : nums) sum += n;
        // cut branch
        if ((sum + target) % 2 != 0 || (sum + target) < 0) return 0;

        // 0-1背包问题
        int bagSize = (sum + target) / 2;
        int[] dp = new int[bagSize + 1];
        dp[0] = 1;

        for (int i : nums) {
            for (int j = bagSize; j >= i; j--) {
                if (dp[j - i] > 0) dp[j] += dp[j-i];
            }
        }

        return dp[bagSize];
    }
}