// 时间复杂度：O(n)，其中 n 是 nums 的长度。
// 虽然我们写了个二重循环，但每次交换都会把一个学生换到正确的座位上，所以总交换次数至多为 n，所以内层循环的总循环次数是 O(n) 的，所以时间复杂度是 O(n)。
// 空间复杂度：O(1)。

class Solution {
    public int firstMissingPositive(int[] nums) {
        int l = nums.length;
        // 1. swap
        for (int i = 0; i < l; i++) {
            // A. we only care about [1, len(nums)], as res in [1, len(nums)+1]
            // B. check if nums[i] in the appropriate idx (i+1 == nums[i])
            // C. check if nums[i] in the target idx (nums[nums[i]-1] == nums[i])
            // D. swap nums[i] to the idx nums[i]-1
            while (nums[i] > 0 && nums[i] <= l && nums[i] != i+1 && nums[nums[i]-1] != nums[i]) {
                int tmp = nums[nums[i] - 1];
                nums[nums[i] - 1] = nums[i];
                nums[i] = tmp;
            }
        }

        // 2. check
        for (int i = 0; i < l; i++) {
            if (nums[i] != i+1) return (i+1);
        }

        return (l+1);
    }
}