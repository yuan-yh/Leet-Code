// Two Pointers
// Time complexity: O(n^2) for double loop, O(nlogn) for sorting, overall O(n^2).
// Space complexity: 
//      O(1) or O(n) extra space depending on the sorting algorithm.
//      O(m) space for the output list.

class Solution {
    public List<List<Integer>> threeSum(int[] nums) {
        List<List<Integer>> res = new ArrayList<>();

        // 1. sort
        Arrays.sort(nums);

        // 2. outer loop i in [0, len-2)
        for (int i = 0; i < nums.length - 2; i++) {
            // 3. short-cut: avoid duplicates || max_sum < 0 || min_sum > 0
            if (i > 0 && nums[i] == nums[i-1]) continue;
            if (nums[i] + nums[nums.length-2] + nums[nums.length-1] < 0) continue;
            if (nums[i] + nums[i+1] + nums[i+2] > 0) break;

            // 4. 2-ptr for inner loop j, k
            int j = i+1, k = nums.length - 1;
            while (j < k) {
                int tmp = nums[i] + nums[j] + nums[k];
                if (tmp < 0) j += 1;
                else if (tmp > 0) k -= 1;
                else {
                    res.add(Arrays.asList(nums[i], nums[j], nums[k]));
                    // 5. avoid duplicates
                    j += 1;
                    k -= 1;
                    while (j < k && nums[j] == nums[j-1]) j += 1;
                    while (j < k && nums[k] == nums[k+1]) k -= 1;
                }
            }
        }

        return res;
    }
}