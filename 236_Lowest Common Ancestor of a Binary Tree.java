// https://www.bilibili.com/video/BV1W44y1Z7AR/?spm_id_from=333.337.search-card.all.click&vd_source=3a9127d6a2a8aebf3636c857ed27ccfa
// DFS
// Time Complexity: O(n)
// Space Complexity: O(n)

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

        TreeNode leftLCA = lowestCommonAncestor(node.left, p, q);
        TreeNode rightLCA = lowestCommonAncestor(node.right, p, q);

        if (leftLCA != null && rightLCA != null) return node;
        else if (leftLCA != null) return leftLCA;
        return rightLCA;
    }
}