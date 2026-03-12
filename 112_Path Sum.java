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
    public boolean hasPathSum(TreeNode root, int target) {
        if (root == null) return false;
        target -= root.val;
        if (root.left == null && root.right == null) return target == 0;
        return this.hasPathSum(root.left, target) || this.hasPathSum(root.right, target);
    }
}