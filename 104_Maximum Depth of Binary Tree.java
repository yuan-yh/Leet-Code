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

// Time Complexity: O(n)
// Space Complexity: O(n)

// Method 1: Recursion
class Solution {
    public int maxDepth(TreeNode root) {
        if (root == null) return 0;

        return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
    }
}

// Method 2: record at the global variable
class Solution {
    private int depth = 0;

    public int maxDepth(TreeNode root) {
        depthHelper(root, 0);
        return depth;
    }

    private void depthHelper(TreeNode node, int curDepth) {
        if (node == null) {
            depth = Math.max(depth, curDepth);
            return;
        }
        depthHelper(node.left, curDepth + 1);
        depthHelper(node.right, curDepth + 1);
    }
}