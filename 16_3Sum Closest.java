// Two Pointers
// Time complexity: O(n^2)
// Space complexity: 
//      O(1) or O(n) extra space depending on the sorting algorithm.
//      O(m) space for the output list.

class Solution {
    public int threeSumClosest(int[] nums, int target) {
        Arrays.sort(nums);
        int res = nums[0] + nums[1] + nums[2];
        for (int i = 0; i < nums.length - 2; i++) {
            // edge case 1: cur + min 2 > target -> the following will definitely even larger and further
            int opt = nums[i] + nums[i+1] + nums[i+2];
            if (opt > target) {
                if (Math.abs(target - opt) < Math.abs(target - res)) res = opt;
                break;
            }
            // edge case 2: cur + max 2 < target -> the following will definitely even smaller and further
            opt = nums[i] + nums[nums.length - 2] + nums[nums.length - 1];
            if (opt < target) {
                if (Math.abs(target - opt) < Math.abs(target - res)) res = opt;
                continue;
            }
            // edge case 3: avoid repeated calculation
            if (i > 0 && nums[i] == nums[i-1]) continue;

            int left = i + 1, right = nums.length - 1;
            while (left < right) {
                int tmp = nums[i] + nums[left] + nums[right];
                if (tmp == target) return tmp;
                if (Math.abs(target - tmp) < Math.abs(target - res)) res = tmp;

                // shift pointers
                if (tmp < target) left++;
                else right--;
            }
        }
        return res;
    }
}