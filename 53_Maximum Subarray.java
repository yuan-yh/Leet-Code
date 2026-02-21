// 时间复杂度：O(n)，其中 n 为 nums 的长度。
// 空间复杂度：O(1)。仅用到若干额外变量。

class Solution {
    public int maxSubArray(int[] nums) {
        int res = nums[0], presum = nums[0];

        for (int i = 1; i < nums.length; i++) {
            presum = Math.max(nums[i], nums[i] + presum);
            res = Math.max(res, presum);
        }

        return res;
    }
}