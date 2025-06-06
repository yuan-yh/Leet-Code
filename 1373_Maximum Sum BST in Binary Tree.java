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
    private int maxSum = 0;

    public int maxSumBST(TreeNode root) {
        // check for BST via post-order
        checkBST(root);
        return maxSum;
    }

    private int[] checkBST(TreeNode node) {
        if (node == null) return new int[]{Integer.MAX_VALUE, Integer.MIN_VALUE, 0};

        int[] left = checkBST(node.left);
        int[] right = checkBST(node.right);

        // case: not BST at its subtrees -> not BST under this node
        if (left[1] == Integer.MAX_VALUE || right[1] == Integer.MAX_VALUE) return new int[]{Integer.MIN_VALUE, Integer.MAX_VALUE, 0};
        // case: not subtree at this node
        if (node.val <= left[1] || node.val >= right[0]) return new int[]{Integer.MIN_VALUE, Integer.MAX_VALUE, 0};
        // case: yes BST at node -> then update curSum then compare with maxSum
        int curSum = node.val + left[2] + right[2];
        maxSum = Math.max(maxSum, curSum);
        return new int[]{Math.min(left[0], node.val), Math.max(right[1], node.val), curSum};
    }
}