// 时间复杂度: O(n^2)
// 空间复杂度: O(n)

class Solution {
    public int lengthOfLIS(int[] nums) {
        int length = nums.length;
        int[] dp = new int[length];
        // init: dp[i] = the longest subsequence ending with nums[i]
        for (int i = 0; i < length; i++) dp[i] = 1;

        // process
        for (int i = 1; i < length; i++) {
            for (int j = 0; j < i; j++) {
                if (nums[j] < nums[i]) dp[i] = Math.max(dp[i], dp[j] + 1);
            }
        }

        int res = 0;
        for (int i : dp) res = Math.max(res, i);
        return res;
    }
}