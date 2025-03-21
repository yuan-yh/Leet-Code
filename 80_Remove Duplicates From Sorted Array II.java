// Time complexity: O(n)
// Space complexity: O(1) extra space

class Solution {
    public int removeDuplicates(int[] nums) {
        int left = 0;   // when left >= 2, it points to the index to be replaced if nums[right] != nums[left-2]
        for (int right = 0; right < nums.length; right++) {
            // case 1: left < 2 
            // case 2: right ptr val != (left-2) ptr val
            if (left < 2 || nums[right] != nums[left - 2]) {
                nums[left] = nums[right];
                left ++;
            }
        }
        return left;
    }
}