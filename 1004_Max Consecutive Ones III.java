// Time complexity: O(n)
// Space complexity: O(1)

class Solution {
    public int longestOnes(int[] nums, int k) {
        int res = 0, count0 = 0, left = 0;

        for (int right = 0; right < nums.length; right++) {
            // 1. count the number of 0s
            count0 += (1 - nums[right]);
            // 2. if exceed k, shift the left pointer
            while (count0 > k) {
                count0 -= (1 - nums[left++]);
            }
            // 3. record the subarray length
            res = Math.max(res, right-left+1);
        }

        return res;
    }
}