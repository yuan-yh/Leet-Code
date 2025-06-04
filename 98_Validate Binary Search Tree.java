// Time complexity: O(n)
// Space complexity: O(n)

// Method 1: Pre-order
class Solution {
    public boolean isValidBST(TreeNode root) {
        return preorder(root, Long.MIN_VALUE, Long.MAX_VALUE);
    }

    private boolean preorder(TreeNode node, long min, long max) {
        if (node == null) return true;

        // check left subtree: update max; check right subtree: update min
        return (node.val > min) && (node.val < max) && preorder(node.left, min, node.val) && preorder(node.right, node.val, max);
    }
}

// Method 2: In-order
class Solution {
    private long prev = Long.MIN_VALUE; 

    public boolean isValidBST(TreeNode root) {
        return inorder(root);
    }

    private boolean inorder(TreeNode node) {
        if (node == null) return true;
        if ((!inorder(node.left)) || (node.val <= prev)) return false;
        prev = node.val;
        return inorder(node.right);
    }
}

// Method 3: Post-order
class Solution {
    public boolean isValidBST(TreeNode root) {
        return (postorder(root)[1] != Long.MAX_VALUE);
    }

    private long[] postorder(TreeNode node) {
        if (node == null) return new long[]{Long.MAX_VALUE, Long.MIN_VALUE};

        long[] left = postorder(node.left);
        long[] right = postorder(node.right);

        // left[1] < node.val < right[0]
        if (node.val <= left[1] || node.val >= right[0] || right[1] == Long.MAX_VALUE) {
            return new long[]{Long.MIN_VALUE, Long.MAX_VALUE};
        }
        return new long[]{Math.min(left[0], node.val), Math.max(right[1], node.val)};
    }
}

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