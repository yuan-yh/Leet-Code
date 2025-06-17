// Time Complexity: O(n^2)
// Space Complexity: O(n)

/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
    private List<List<Integer>> res = new ArrayList<>();
    private List<Integer> cur = new ArrayList<>();

    public List<List<Integer>> pathSum(TreeNode root, int targetSum) {
        bt(root, targetSum);
        return res;
    }

    private void bt(TreeNode n, int target) {
        if (n == null) return;
        
        cur.add(n.val);

        // end case: leaf
        if (n.left == null && n.right == null) {
            if (target == n.val) res.add(new ArrayList<>(cur));
        } 
        else {
            // process
            bt(n.left, target - n.val);
            bt(n.right, target - n.val);
        }
        // backtrack
        cur.remove(cur.size() - 1);
    }
}