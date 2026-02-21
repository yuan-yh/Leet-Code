// 时间复杂度：O(n)，其中 n 是 nums 的长度。
// 空间复杂度：O(1)。

class Solution {
    private void mirror(int[] nums, int left, int right) {
        while (left < right) {
            int tmp = nums[left];
            nums[left++] = nums[right];
            nums[right--] = tmp;
        }
    }

    public void rotate(int[] nums, int k) {
        // 1. min k
        k = k % nums.length;
        
        // 2. mirror nums[:]
        mirror(nums, 0, nums.length - 1);
        
        // 3. mirror nums[:k) and nums[k:]
        mirror(nums, 0, k - 1);
        mirror(nums, k, nums.length - 1);
    }
}