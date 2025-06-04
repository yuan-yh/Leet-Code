// Time Complexity: O(n)
// Space Complexity: O(n)

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
    public boolean isUnivalTree(TreeNode root) {
        // compare the cur node with its children, then look into subtrees
        if (root == null) return true;

        return ((root.left == null) ? true : (root.val == root.left.val)) && ((root.right == null) ? true : (root.val == root.right.val)) && isUnivalTree(root.left) && isUnivalTree(root.right);
    }
}