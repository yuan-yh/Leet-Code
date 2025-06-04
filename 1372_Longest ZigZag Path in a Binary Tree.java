// Time Complexity: O(n)
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
    private int maxLength = 0;

    public int longestZigZag(TreeNode root) {
        dfs(root.left, true);
        dfs(root.right, false);
        return maxLength;
    }

    private int dfs(TreeNode node, boolean prevLeft) {
        if (node == null) return 0;

        int left = dfs(node.left, true) + 1;
        int right = dfs(node.right, false) + 1;

        if (prevLeft) {
            maxLength = Math.max(maxLength, right);
            return right;
        } else {
            maxLength = Math.max(maxLength, left);
            return left;
        }
    }
}