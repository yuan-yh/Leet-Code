// Time complexity: O(log(n))
// Space complexity: O(1)

class Solution {
    public int findMin(int[] nums) {
        // label [start, ..., a[n-1],] as RED and [a[0], ..., end] as BLUE
        // the goal is to find the first BLUE

        int left = 0, right = nums.length - 1;

        while (left < right) {
            int mid = left + (right - left) / 2;
            // [mid, right] is BLUE
            if (nums[mid] < nums[right]) right = mid;
            // [mid, right] is RED + BLUE && nums[mid] is RED
            else left = mid + 1;
        }

        return nums[right];
    }
}