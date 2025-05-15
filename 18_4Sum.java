// double for loop -> 2 pointer
// Time complexity: O(n^3)
// Space complexity: 
//      O(1) or O(n) extra space depending on the sorting algorithm.
//      O(m) space for the output list.

class Solution {
    public List<List<Integer>> fourSum(int[] nums, int target) {
        Arrays.sort(nums);
        List<List<Integer>> res = new ArrayList<>();

        for (int a = 0; a < nums.length - 3; a++) {
            // can be edge case optimization
            // edge case 1: cur + min 3 > target
            long opt = nums[a];
            if (opt + nums[a+1] + nums[a+2] + nums[a+3] > target) break;
            // edge case 2: cur + max 3 < target
            if (opt + nums[nums.length - 3] + nums[nums.length - 2] + nums[nums.length - 1] < target) continue;
            // edge case 3: avoid repetition
            if (a > 0 && nums[a] == nums[a-1]) continue;

            for (int b = a+1; b < nums.length - 2; b++) {
                // can be edge case optimization
                // edge case 1: cur + min 2 > target
                long opt2 = nums[b];
                if (opt + opt2 + nums[b+1] + nums[b+2] > target) break;
                // edge case 2: cur + max 2 < target
                if (opt + opt2 + nums[nums.length - 2] + nums[nums.length - 1] < target) continue;
                // edge case 3: avoid repetition
                if (b > a+1 && nums[b] == nums[b-1]) continue;

                int left = b + 1, right = nums.length - 1;

                // shift pointer
                while (left < right) {
                    long tmp = nums[a] + nums[b] + nums[left] + nums[right];

                    if (tmp < target) left++;
                    else if (tmp > target) right--;
                    else {
                        res.add(Arrays.asList(nums[a], nums[b], nums[left], nums[right]));
                        left++;
                        right--;
                        while (left < right && nums[left] == nums[left-1]) left++;
                        while (left < right && nums[right] == nums[right+1]) right--;
                    }
                }
            }
        }

        return res;
    }
}