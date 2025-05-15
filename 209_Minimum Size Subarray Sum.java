// Time complexity: O(n)
// Space complexity: O(1)

class Solution {
    public int minSubArrayLen(int target, int[] nums) {
        int left = 0, sum = 0, minLength = nums.length + 1;

        for (int right = 0; right < nums.length; right++) {
            sum += nums[right];

            // record the subarray length once reached the target
            // shift the left pointer
            while (left <= right && sum >= target) {
                minLength = Math.min(minLength, right-left+1);

                // opt case: return if find the opt answer
                if (minLength == 1) return minLength;

                sum -= nums[left];
                left++;
            }
            
        }

        return (minLength == nums.length + 1) ? 0 : minLength;
    }
}