// Time Complexity: O(n * 2^n)
// Space Complexity: O(n)

// Essentially it traverses through each leaf of a binary tree, in which at each node is two choices: add the cur digit or not
// Therefore, we choose a branch, then backtrack the choice and turn to a different branch

class Solution {
    List<List<Integer>> res = new ArrayList<>();
    List<Integer> cur = new ArrayList<>();
    int[] nums;

    public List<List<Integer>> subsets(int[] nums) {
        this.nums = nums;
        bt(0);
        return res;
    }

    private void bt(int start) {
        // end case
        if (start == nums.length) {
            res.add(new ArrayList<>(cur));
            return;
        }
        // process
        cur.add(nums[start]);
        bt(start + 1);
        // backtrack
        cur.remove(cur.size() - 1);
        bt(start + 1);
    }
}