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
    private int count = 0;

    public int diameterOfBinaryTree(TreeNode root) {
        dfs(root);
        return count;
    }

    private int dfs(TreeNode node) {
        // end case: null
        if (node == null) return 0;

        // measure left and right length
        int left = dfs(node.left);
        int right = dfs(node.right);

        // update diameter if passing from left through the current node to right
        count = Math.max(count, left + right);
        return (1 + Math.max(left, right));
    }
}
