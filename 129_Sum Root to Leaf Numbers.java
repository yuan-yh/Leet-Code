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
    private int res = 0;

    public int sumNumbers(TreeNode root) {
        helper(root, 0);
        return res;
    }

    private void helper(TreeNode node, int n) {
        // case: empty node
        if (node == null) return;
        // case: leaf node
        if (node.left == null && node.right == null) {
            res += n*10 + node.val;
            return;
        }
        helper(node.left, n * 10 + node.val);
        helper(node.right, n * 10 + node.val);
    }
}