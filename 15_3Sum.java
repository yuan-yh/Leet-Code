// Two Pointers
// Time complexity: O(n^2)
// Space complexity: 
//      O(1) or O(n) extra space depending on the sorting algorithm.
//      O(m) space for the output list.

class Solution {
    public List<List<Integer>> threeSum(int[] nums) {
        List<List<Integer>> res = new ArrayList<>();
        Arrays.sort(nums);
        
        // 1st digit - for loop; have to be negative || zero
        for (int i = 0; i < nums.length && nums[i] <= 0; i++) {
            // avoid duplicates
            if (i > 0 && nums[i] == nums[i-1]) continue;

            // 2nd & 3rd digit - two-pointer: [1st+1, the last]
            int l = i+1, r = nums.length-1;
            while (l < r) {
                int tmp = nums[i] + nums[l] + nums[r];
                if (tmp > 0) r--;
                else if (tmp < 0) l++;
                else {
                    res.add(Arrays.asList(nums[i], nums[l], nums[r]));
                    // update l & r while avoid duplicate values
                    l++;
                    r--;
                    while (l < r && nums[l] == nums[l-1]) l++;
                }
            }
        }
        return res;
    }
}