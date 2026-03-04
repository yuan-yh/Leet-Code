// DFS
// Time complexity: O(n)
// Space complexity: O(h)
//     Best Case (balanced tree): O(log(n))
//     Worst Case (degenerate tree): O(n)
// Where is the number of nodes in the tree and h is the height of the tree.

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
    private int diameter = 0;

    private int dfs(TreeNode node) {
        if (node == null) return -1;
        int left = dfs(node.left) + 1, right = dfs(node.right) + 1;
        this.diameter = Math.max(this.diameter, left + right);
        return Math.max(left, right);
    }

    public int diameterOfBinaryTree(TreeNode root) {
        dfs(root);
        return this.diameter;
    }
}
