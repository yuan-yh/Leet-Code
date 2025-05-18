class Solution {
    public int[] searchRange(int[] nums, int target) {
        int[] res = new int[]{-1, -1};

        // O(log n) -> binary search
        int first = leftBoundary(nums, target);

        if (first != nums.length && nums[first] == target) {
            int last = rightBoundary(nums, target);
            res[0] = first;
            res[1] = last;
        }

        return res;
    }

    // return the first position of element >= target in sorted array, or the array length if not exist
    // RED: element < target; BLUE: element >= target
    // m < target -> left = m + 1 -> left-1 : RED
    // m >= target -> right = m - 1 -> right+1: BLUE
    // output: the index of first BLUE -> right+1 = left
    private int leftBoundary(int[] nums, int target) {
        int left = 0, right = nums.length - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (nums[mid] < target) left = mid+1;  // left-1: RED
            else right = mid-1;                    // right+1: BLUE
        }
        return left;                               // the first BLUE
    }

    // return the last position of element <= target in sorted array
    // RED: element <= target; BLUE: element > target
    // m > target -> right = m - 1 -> right+1: BLUE
    // m <= target -> left = m + 1 -> left-1 : RED
    // output: the index of last RED -> right+1-1 = left-1
    private int rightBoundary(int[] nums, int target) {
        int left = 0, right = nums.length - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (nums[mid] > target) right = mid-1; // right+1: BLUE
            else left = mid+1;                     // left-1: RED
        }
        return right;                               // the last RED
    }
}