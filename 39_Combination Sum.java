class Solution {
    private List<List<Integer>> res = new ArrayList<>();
    private List<Integer> curPath = new ArrayList<>();
    private int[] candidates;

    private void bt(int idx, int left) {
        // end case
        if (left == 0) {
            res.add(new ArrayList<>(curPath));
            return;
        }
        // process
        for (int i = idx; i < candidates.length; i++) {
            // short-cut: terminate if beyond target
            if (candidates[i] > left) break;
            // short-cut: skip to avoid duplicates
            if (i > idx && candidates[i] == candidates[idx]) continue;

            curPath.add(candidates[i]);
            bt(i, left - candidates[i]);
            curPath.remove(curPath.size() - 1);
        }
    }

    public List<List<Integer>> combinationSum(int[] candidates, int target) {
        this.candidates = candidates;
        // 1. sort
        Arrays.sort(candidates);
        // 2. process
        bt(0, target);
        return this.res;
    }
}