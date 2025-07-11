// Time complexity: O(n+m)，其中 n 为二叉树的节点个数，m 为 toDelete 的长度。每个节点都会递归恰好一次。
// Space complexity: O(n+m)

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
    public List<TreeNode> delNodes(TreeNode root, int[] to_delete) {
        Set<Integer> toDel = new HashSet<>();
        for (int i : to_delete) toDel.add(i);
        List<TreeNode> res = new ArrayList<>();

        // check the subtree
        // check the curNode val
        //  if yes: add into list if not null
        //  if no: assign back to the curNode
        TreeNode tmp = dfs(root, toDel, res);
        if (tmp != null) res.add(tmp);
        return res;
    }

    private TreeNode dfs(TreeNode node, Set<Integer> del, List<TreeNode> res) {
        if (node == null) return node;

        node.left = dfs(node.left, del, res);
        node.right = dfs(node.right, del, res);

        if (!del.contains(node.val)) return node;
        if (node.left != null) res.add(node.left);
        if (node.right != null) res.add(node.right);
        return null;
    }
}