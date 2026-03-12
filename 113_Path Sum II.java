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
    private List<List<Integer>> res;
    private List<Integer> curPath;

    private void bt(TreeNode node, int target) {
        if (node == null) return;

        curPath.add(node.val);
        target -= node.val;

        if (node.left == null && node.right == null) {
            if (target == 0) res.add(new ArrayList<>(curPath));
            curPath.remove(curPath.size()-1);
            return;
        }

        bt(node.left, target);
        bt(node.right, target);
        curPath.remove(curPath.size()-1);
    }

    public List<List<Integer>> pathSum(TreeNode root, int targetSum) {
        this.res = new ArrayList<>();
        this.curPath = new ArrayList<>();

        bt(root, targetSum);
        return this.res;
    }
}