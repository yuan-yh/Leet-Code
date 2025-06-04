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
    public boolean flipEquiv(TreeNode n1, TreeNode n2) {
        // check the cur node, then corresponding children nodes
        if (n1 == null || n2 == null) return (n1 == n2);

        return ((n1.val == n2.val) && ((flipEquiv(n1.left, n2.left) && flipEquiv(n1.right, n2.right)) || (flipEquiv(n1.left, n2.right) && flipEquiv(n1.right, n2.left))));
    }
}