class Solution {
    private List<List<Integer>> res = new ArrayList<>();
    private List<Integer> cur = new ArrayList<>();
    private int[] nums;

    public List<List<Integer>> combinationSum(int[] candidates, int target) {
        this.nums = candidates;
        bt(0, target);
        return res;
    }

    private void bt(int startIndex, int target) {
        // end case
        if (target == 0) {
            res.add(new ArrayList<>(cur));
            return;
        }
        // cut branch
        if (target < 0) return;
        // process & backtrack
        for (int i = startIndex; i < nums.length; i++) {
            cur.add(nums[i]);
            bt(i, target - nums[i]);
            cur.remove(cur.size() - 1);
        }
    }
}