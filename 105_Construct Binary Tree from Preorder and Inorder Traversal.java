// Time complexity: O(n), 其中 n 为 preorder 的长度。递归 O(n) 次，每次只需要 O(1) 的时间。
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
    private int[] preorder;
    private Map<Integer, Integer> idx;

    private TreeNode dfs(int pl, int pr, int il) {
        if (pl >= pr) return null;

        TreeNode root = new TreeNode(this.preorder[pl]);

        int i = this.idx.get(this.preorder[pl]);
        int leftSize = i - il;

        root.left = this.dfs(pl+1, pl+1+leftSize, il);
        root.right = this.dfs(pl+1+leftSize, pr, i+1);
        return root;
    }

    public TreeNode buildTree(int[] preorder, int[] inorder) {
        this.preorder = preorder;
        this.idx = new HashMap<>();
        for (int i = 0; i < inorder.length; i++) this.idx.put(inorder[i], i);
        
        return dfs(0, preorder.length, 0);
    }
}