// Binary Search (One Pass)
// Time complexity: O(logn)
// Space complexity: O(1)

class Solution {
    public int search(int[] nums, int target) {
        int left = 0, right = nums.length - 1;

        while (left <= right) {
            int mid = left + (right - left) / 2;

            // case: find the target
            if (nums[mid] == target) return mid;

            // [mid, right] sorted
            if (nums[mid] < nums[right]) {
                // check if target in [mid, right]
                if (nums[mid] < target && target <= nums[right]) left = mid + 1;
                else right = mid - 1;
            }
            // [left, mid] sorted
            else {
                // check if target in [left, mid]
                if (nums[left] <= target && target < nums[mid]) right = mid - 1;
                else left = mid + 1;
            }
        }

        return -1;
    }
}