// Time Complexity: O(k * C(9,k))
// Space Complexity: O(n)

class Solution {
    private List<List<Integer>> res = new ArrayList<>();
    private List<Integer> cur = new ArrayList<>();

    public List<List<Integer>> combinationSum3(int k, int n) {
        bt(1, k, n);
        return res;
    }

    private void bt(int start, int numsLeft, int target) {
        // end case
        if (numsLeft == 0 && target == 0) {
            res.add(new ArrayList<>(cur));
            return;
        }
        // cut branch: 1) large curSum; 2) impossible to add up to the target - (k1+kn)*(n)/2
        if (numsLeft == 0 || target <= 0 || target > (19 - numsLeft)*numsLeft / 2) return;

        for (int i = start; i <= 9; i++) {
            // process
            cur.add(i);
            bt(i+1, numsLeft-1, target-i);
            // backtrack
            cur.remove(cur.size() - 1);
        }
    }
}