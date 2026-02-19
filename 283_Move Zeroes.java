// 时间复杂度：O(n)，其中 n 是 nums 的长度。
// 空间复杂度：O(1)

class Solution {
    public void moveZeroes(int[] nums) {
        int slow = 0;
        for (int fast = 0; fast < nums.length; fast ++) {
            if (nums[fast] != 0) {
                nums[slow] = nums[fast];
                slow += 1;
            }
        }
        for (int i = slow; i < nums.length; i++) nums[i] = 0;
    }
}