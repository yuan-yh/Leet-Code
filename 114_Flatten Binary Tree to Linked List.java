// 时间复杂度：O(n)，其中 n 是二叉树的节点个数。
// 空间复杂度：O(n)。递归需要 O(n) 的栈空间。

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
    private TreeNode head = null;

    public void flatten(TreeNode root) {
        if (root == null) return;

        this.flatten(root.right);
        this.flatten(root.left);

        root.left = null;
        root.right = this.head;
        this.head = root;
    }
}