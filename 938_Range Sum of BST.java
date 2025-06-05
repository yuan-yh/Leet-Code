// Time complexity: O(n)
// Space complexity: O(n)

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
    public int rangeSumBST(TreeNode root, int low, int high) {
        // node > [low, high] -> node.right must be outside of the given range
        // node < [low, high] -> node.left must be outside of the given range

        if (root == null) return 0;
        return (
            ((root.val >= low && root.val <= high) ? root.val : 0) + 
            ((root.val < low) ? 0 : rangeSumBST(root.left, low, high)) + 
            ((root.val > high) ? 0 : rangeSumBST(root.right, low, high)));
    }
}