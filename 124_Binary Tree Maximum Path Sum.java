// 时间复杂度：O(n)，其中 n 为二叉树的节点个数。
// 空间复杂度：O(n)。最坏情况下，二叉树退化成一条链，递归需要 O(n) 的栈空间。

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
    private int res = Integer.MIN_VALUE;

    private int postOrder(TreeNode node) {
        if (node == null) return 0;
        int l = postOrder(node.left), r = postOrder(node.right);

        this.res = Math.max(this.res, l + r + node.val);
        return Math.max(Math.max(l, r) + node.val, 0);
    }

    public int maxPathSum(TreeNode root) {
        postOrder(root);
        return this.res;
    }
}