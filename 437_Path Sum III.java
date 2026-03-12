// 时间复杂度：O(n)，其中 n 是二叉树的节点个数。
// 空间复杂度：O(n)。

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
    private Map<Long, Integer> prefix;
    private int cnt, target;

    private void bt(TreeNode node, long curSum) {
        if (node == null) return;

        curSum += node.val;
        if (this.prefix.containsKey(curSum - this.target)) this.cnt += this.prefix.get(curSum - this.target);

        this.prefix.put(curSum, this.prefix.getOrDefault(curSum, 0) + 1);
        bt(node.left, curSum);
        bt(node.right, curSum);
        this.prefix.put(curSum, this.prefix.get(curSum) - 1);
    }

    public int pathSum(TreeNode root, int targetSum) {
        this.prefix = new HashMap<>();
        this.prefix.put(0L, 1);
        this.cnt = 0;
        this.target = targetSum;

        bt(root, 0);
        return this.cnt;
    }
}