// 时间复杂度：O(n)，其中 n 为二叉树的节点个数。每个节点都会递归恰好一次。
// 空间复杂度：O(n)。最坏情况下，二叉树是一条链，递归需要 O(n) 的栈空间。

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
    public int goodNodes(TreeNode root) {
        return helper(root, Integer.MIN_VALUE);
    }

    private int helper(TreeNode node, int n) {
        if (node == null) return 0;

        return (helper(node.left, Math.max(n, node.val)) + helper(node.right, Math.max(n, node.val))) + ((node.val >= n) ? 1 : 0);
    }
}