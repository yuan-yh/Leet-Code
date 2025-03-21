// Time complexity: O(n)
// Space complexity: O(1)

class Solution {
    public int removeDuplicates(int[] nums) {
        // point to the last non-repeated digit
        int slow = 0;
        // iterate through the rest array
        for (int fast = 1; fast < nums.length; fast++) {
            if (nums[slow] != nums[fast]) {
                slow ++;
                nums[slow] = nums[fast];
            }
        }
        return slow + 1;
    }
}