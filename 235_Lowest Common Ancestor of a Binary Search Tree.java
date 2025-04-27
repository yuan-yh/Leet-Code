// https://www.bilibili.com/video/BV1W44y1Z7AR/?spm_id_from=333.337.search-card.all.click&vd_source=3a9127d6a2a8aebf3636c857ed27ccfa
// DFS
// Time Complexity: O(N)
// Space Complexity: O(N)

/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode(int x) { val = x; }
 * }
 */

class Solution {
    public TreeNode lowestCommonAncestor(TreeNode node, TreeNode p, TreeNode q) {
        if (node == null || node == p || node == q) return node;

        // 3 cases based on the BST: both < - left tree; both > - right tree; in-between - current node is LCA
        if (p.val < node.val && q.val < node.val) return lowestCommonAncestor(node.left, p, q);
        if (p.val > node.val && q.val > node.val) return lowestCommonAncestor(node.right, p, q);
        return node;
    }
}