// Backtracking (Optimal)
// Time complexity: O(n!∗n)
// Space complexity: O(n!∗n) for the output list

class Solution {
    List<List<Integer>> res;

    public List<List<Integer>> permute(int[] nums) {
        res = new ArrayList<>();
        backtrack(nums, 0);
        return res;
    }

    private void backtrack(int[] nums, int index) {
        // end case: complete the re-arrangment of nums
        if (index == nums.length) {
            List<Integer> list = new ArrayList<>();
            for (int n : nums) list.add(n);
            res.add(list);
            return;
        }
        // process & retrieve
        for (int i = index; i < nums.length; i++) {
            swap(nums, i, index);   // determine the digit at index i
            backtrack(nums, index + 1);
            swap(nums, i, index);   // backtrack
        }
    }

    private void swap(int[] nums, int p1, int p2) {
        int tmp = nums[p1];
        nums[p1] = nums[p2];
        nums[p2] = tmp;
    }
}