// Two Pointers
// Time complexity: O(n^2)
// Space complexity: 
//      O(1) or O(n) extra space depending on the sorting algorithm.
//      O(m) space for the output list.

class Solution {
    public List<List<Integer>> threeSum(int[] nums) {
        List<List<Integer>> res = new ArrayList<>();
        // the order of the output not matter
        Arrays.sort(nums);

        for (int i = 0; i < nums.length-2; i++) {
            // edge case for optimization: the 3 smallest digits in the cur range > 0 -> break
            if (nums[i] + nums[i+1] + nums[i+2] > 0) break;
            // edge case for optimization: the cur + 2 largest digits < 0 -> continue
            if (nums[i] + nums[nums.length-2] + nums[nums.length-1] < 0) continue;

            // avoid repetition for the first digit
            if (i > 0 && nums[i] == nums[i-1]) continue;

            int left = i+1, right = nums.length-1;
            while (left < right) {
                int tmp = nums[left] + nums[right];

                if (tmp < (0 - nums[i])) left++;
                else if (tmp > (0 - nums[i])) right--;
                else {
                    res.add(Arrays.asList(nums[i], nums[left], nums[right]));
                    left++;
                    right--;
                    // avoid repetition
                    while (left < right && nums[left] == nums[left-1]) left++;
                }
            }
        }

        return res;
    }
}