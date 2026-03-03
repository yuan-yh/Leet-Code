// 时间复杂度：O(n)
// 空间复杂度：O(n) -- 最差情况下（二叉树退化为链表）
 
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
    private boolean check(TreeNode n1, TreeNode n2) {
        if (n1 == null && n2 == null) return true;
        if (n1 == null || n2 == null || n1.val != n2.val) return false;

        return (check(n1.left, n2.right) && check(n1.right, n2.left));
    }

    public boolean isSymmetric(TreeNode root) {
        return check(root.left, root.right);
    }
}