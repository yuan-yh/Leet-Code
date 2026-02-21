// 时间复杂度：O(n)，其中 n 是 nums 的长度。
// 空间复杂度：O(1)。返回值不计入。

class Solution {
    public int[] productExceptSelf(int[] nums) {
        int l = nums.length, pre = 1, post = 1;
        int[] res = new int[l];

        // 1. pre-product
        for (int i = 0; i < l; i++) {
            res[i] = pre;
            pre *= nums[i];
        }

        // 2. post-product
        for (int i = l-1; i >= 0; i--) {
            res[i] *= post;
            post *= nums[i];
        }

        return res;
    }
}