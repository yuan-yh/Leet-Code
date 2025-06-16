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
    public TreeNode replaceValueInTree(TreeNode root) {
        // sum - curNode
        root.val = 0;
        List<TreeNode> parent = new ArrayList<>();
        parent.add(root);

        while (!parent.isEmpty()) {
            int sum = 0;
            List<TreeNode> children = new ArrayList<>();

            // count children node sum
            for (TreeNode n : parent) {
                if (n.left != null) {
                    sum += n.left.val;
                    children.add(n.left);
                }
                if (n.right != null) {
                    sum += n.right.val;
                    children.add(n.right);
                }
            }

            // calculate cousin sum
            for (TreeNode n : parent) {
                int childSum = (n.left == null ? 0 : n.left.val) + (n.right == null ? 0 : n.right.val);
                if (n.left != null) n.left.val = sum - childSum;
                if (n.right != null) n.right.val = sum - childSum;
            }

            // update parent to children
            parent = children;
        }
        return root;
    }
}