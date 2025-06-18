// Time Complexity: O(k * C(n,k))
// Space Complexity: O(n)

class Solution {
    private List<List<Integer>> res = new ArrayList<>();
    private List<Integer> cur = new ArrayList<>();

    public List<List<Integer>> combine(int n, int k) {
        bt(1, n, k); 
        return res;
    }

    private void bt(int start, int end, int numsLeft) {
        // end case
        if (numsLeft == 0) {
            res.add(new ArrayList<>(cur));
            return;
        }
        // cut branch
        if (end - start + 1 < numsLeft) return;

        for (int i = start; i <= end; i++) {
            // process
            cur.add(i);
            bt(i+1, end, numsLeft-1);
            // backtrack
            cur.remove(cur.size() - 1);
        }
    }
}