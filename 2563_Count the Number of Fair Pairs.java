// Time complexity: O(nlog(n))
// Space complexity: O(1)

class Solution {
    public long countFairPairs(int[] nums, int lower, int upper) {
        // 1. sort the given array, as we only look for total number of pairs
        Arrays.sort(nums);

        // 2. two-pointer + binary search
        long res = 0;

        for (int j = 1; j < nums.length; j++) {
            // 0 <= i < j < n --> so j starts from 1, and i in [0, j-1]
            // lower - nums[j] <= nums[i] <= upper - nums[j]

            // the first index of element >= lower - nums[j]
            int left = bs(nums, 0, j-1, lower - nums[j]);           
            // one before the first index of element >= upper - nums[j] + 1 == the last element <= upper - nums[j]
            int right = bs(nums, 0, j-1, upper - nums[j] + 1) - 1;  

            res += (right - left + 1);
        }
        return res;
    }

    // return the index of first element >= target
    private int bs(int[] nums, int left, int right, int target) {
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (nums[mid] < target) left = mid + 1;
            else right = mid - 1;
        }
        return left;
    }
}