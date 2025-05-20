// Time complexity: O(log(n))
// Space complexity: O(1)

class Solution {
    public int findPeakElement(int[] nums) {
        // Label 'left of peak' as RED and 'peak and rightwards' as BLUE
        // Assume the peak exists, the last digit must be BLUE
        // the goal is to find the index of the 1st BLUE
        int left = 0, right = nums.length - 1;

        while (left <= right) {
            int mid = left + (right - left) / 2;

            if (mid+1 < nums.length && nums[mid] < nums[mid+1]) left = mid + 1;
            else right = mid - 1;
        }

        return left;
    }
}