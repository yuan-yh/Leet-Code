// Time complexity: O(n)
// Space complexity: O(1)

class Solution {
    public int numSubarrayProductLessThanK(int[] nums, int k) {
        // edge case: k < 1 as all nums[i] are positive integers
        if (k < 1) return 0;

        int left = 0, res = 0;
        long product = 1;

        for (int right = 0; right < nums.length; right++) {
            product *= nums[right];

            while (left <= right && product >= k) {
                product /= nums[left];
                left ++;
            }
            // update res for each valid case: count the number of subarray including the last digit
            res += (right - left + 1);
        }

        return res;
    }
}