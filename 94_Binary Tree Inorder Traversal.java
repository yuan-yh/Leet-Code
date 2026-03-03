// 时间复杂度：O(n)，其中 n 是二叉树的节点个数。
// 空间复杂度：O(h)，其中 h 是二叉树的高度。递归需要 O(h) 的栈空间。返回值不计入。

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
    private void inorder(List<Integer> res, TreeNode node) {
        if (node == null) return;

        inorder(res, node.left);
        res.add(node.val);
        inorder(res, node.right);
    }

    public List<Integer> inorderTraversal(TreeNode root) {
        List<Integer> res = new ArrayList<>();
        inorder(res, root);
        return res;
    }
}