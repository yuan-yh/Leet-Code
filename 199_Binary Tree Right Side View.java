// 时间复杂度：O(n)
// 空间复杂度：O(n)

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
    public List<Integer> rightSideView(TreeNode root) {
        List<Integer> res = new ArrayList<>();
        dfs(root, 0, res);
        return res;
    }

    private void dfs(TreeNode node, int depth, List<Integer> res) {
        // end case - empty node
        if (node == null) return;
        // traversal: mid -> right -> left
        // case: new depth == res.size() -> record the new value
        if (depth == res.size()) res.add(node.val);
        dfs(node.right, depth + 1, res);
        dfs(node.left, depth + 1, res);
    }
}