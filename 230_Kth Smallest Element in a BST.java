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
    private int res;
    private int k;

    public int kthSmallest(TreeNode root, int k) {
        this.k = k;
        inorder(root);
        return res;
    }

    private void inorder(TreeNode node) {
        if (node == null || k == 0) return;

        inorder(node.left);

        k -= 1;
        if (k == 0) res = node.val;
        
        inorder(node.right);
    }
}