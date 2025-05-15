// Time complexity: O(n)
// Space complexity: O(1)

class Solution {
    public long countSubarrays(int[] nums, int k) {
        // 1. find the max element
        int max = nums[0];
        for (int n : nums) max = Math.max(max, n);

        // 2. find the number of subarray having at least k max-element
        int left = 0, maxCount = 0;
        long res = 0;

        for (int right = 0; right < nums.length; right++) {
            if (nums[right] == max) maxCount ++;

            while (maxCount == k) {
                if (nums[left] == max) maxCount--;
                left++; 
            }
            // all subarray from [0, right] to [left-1, right] meet the requirement: maxCount >= k
            res += left;
        }

        return res;
    }
}