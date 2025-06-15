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
    public int minDepth(TreeNode root) {
        if (root == null) return 0;
        int res = 0, cur = 0, size;
        Queue<TreeNode> q = new LinkedList<>();
        q.add(root);

        while (!q.isEmpty()) {
            cur ++;
            size = q.size();
            for (int i = 0; i < size; i++) {
                TreeNode n = q.poll();
                if (n.left == null && n.right == null) {
                    res = cur;
                    break;
                }
                if (n.left != null) q.add(n.left);
                if (n.right != null) q.add(n.right);
            }
            if (res != 0) break;
        }

        return res;
    }
}