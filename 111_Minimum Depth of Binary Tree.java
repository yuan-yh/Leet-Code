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
    private int res = Integer.MAX_VALUE;

    public int minDepth(TreeNode root) {
        depthHelper(root, 0);
        return (root == null) ? 0 : res;
    }

    private void depthHelper(TreeNode node, int curDepth) {
        // end case: empty node
        if (node == null) return;
        // end case: leaf node
        if (node.left == null && node.right == null) {
            res = Math.min(res, curDepth + 1);
            return;
        }
        // process
        depthHelper(node.left, curDepth + 1);
        depthHelper(node.right, curDepth + 1);
    }
}