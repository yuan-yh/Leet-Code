// Time complexity: O(n)
// Space complexity: O(1)

class Solution {
    public int[] twoSum(int[] nums, int target) {
        int left = 0, right = nums.length - 1;
        while (left < right) {
            int sum = nums[left] + nums[right];

            if (sum < target) left++;
            else if (sum > target) right--;
            else break;
        }
        return new int[]{left+1, right+1};
    }
}