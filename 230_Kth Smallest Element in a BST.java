// 时间复杂度：O(n)，其中 n 是二叉树的大小（节点个数）。
// 空间复杂度：O(h)，其中 h 是树高，递归需要 O(h) 的栈空间。最坏情况下树是一条链，h=n，空间复杂度为 O(n)。

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
    private int k;

    private int inorder(TreeNode node) {
        if (node == null) return -1;

        int left = this.inorder(node.left);
        if (left != -1) return left;

        this.k -= 1;
        if (this.k == 0) return node.val;

        return this.inorder(node.right);
    }

    public int kthSmallest(TreeNode root, int k) {
        this.k = k;
        return this.inorder(root);
    }
}