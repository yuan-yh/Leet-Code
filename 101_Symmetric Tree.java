// 时间复杂度：O(n)
// 空间复杂度：O(n)
 
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
    public boolean isSymmetric(TreeNode root) {
        return symmetricHelper(root.left, root.right);
    }

    private boolean symmetricHelper(TreeNode p, TreeNode q) {
        // Given symmetric: left-subtree-left vs right-subtree-right, left-subtree-right vs right-subtree-left
        if (p == null || q == null) return (p == q);

        return (p.val == q.val) && (symmetricHelper(p.left, q.right)) && (symmetricHelper(p.right, q.left));
    }
}