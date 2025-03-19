// Binary Search (One Pass)
// Time complexity: O(logn)
// Space complexity: O(1)

class Solution {
    public int search(int[] nums, int target) {
        int left = 0, right = nums.length - 1;
        while (left <= right) {
            int middle = (right - left) / 2 + left;

            if (nums[middle] == target) return middle;
            // left - middle sorted, possible right rotated
            if (nums[left] <= nums[middle]) {
                if (nums[left] <= target && target < nums[middle]) {
                    right = middle - 1;
                } else {
                    left = middle + 1;
                }
            }
            // left - middle rotated, right sorted
            else {
                if (nums[middle] < target && target <= nums[right]) {
                    left = middle + 1;
                }
                else {
                    right = middle - 1;
                }
            }
        }
        return -1;
    }
}