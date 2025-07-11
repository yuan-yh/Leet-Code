// 时间复杂度：O(ns)，其中 n 是 nums 的长度，s 是 nums 的元素和（的一半）。
// 空间复杂度：O(s)

class Solution {
    public boolean canPartition(int[] nums) {
        int target = 0;
        // 1. count sum and determine edge case for odd sum
        for (int n : nums) target += n;
        if (target %2 != 0) return false;
        target /= 2;
        // 2. fill the bag with size 'target'
        int[] dp = new int[target + 1];

        for (int n : nums) {
            for (int j = target; j >= n; j--) {
                dp[j] = Math.max(dp[j], dp[j-n] + n);
                // cut branch
                if (dp[j] == target) return true;
            }
        }

        return (dp[target] == target);
    }
}