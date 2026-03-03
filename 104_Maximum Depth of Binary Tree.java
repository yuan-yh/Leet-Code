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
        return (root == null) ? 0 : 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
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

// Method 3: BFS
class Solution {
    public int maxDepth(TreeNode root) {
        Queue<TreeNode> q = new LinkedList<>();
        if (root != null) q.add(root);
        int res = 0;

        while (!q.isEmpty()) {
            int cnt = q.size();
            res += 1;
            for (int i = 0; i < cnt; i++) {
                TreeNode tmp = q.poll();
                if (tmp.left != null) q.add(tmp.left);
                if (tmp.right != null) q.add(tmp.right);
            }
        }

        return res;
    }
}