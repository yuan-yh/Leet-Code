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
    public TreeNode buildTree(int[] preorder, int[] inorder) {
        // in the given range of preorder: 
        //      preorder[0] = curNode
        //      preorder[1:] = curNode.left + curNode.right
        // in the given range of inorder:
        //      locate the curNode
        //      inorder[0 : cur) = curNode.left
        //      inorder[cur+1:] = curNode.right

        int total = preorder.length;
        Map<Integer, Integer> index = new HashMap<>(total);
        // 1. record node index to locate the current root node
        for (int i = 0; i < total; i++) index.put(inorder[i], i);
        return dfs(preorder, 0, total, inorder, 0, total, index);
    }

    private TreeNode dfs(int[] preorder, int pLeft, int pRight, int[] inorder, int iLeft, int iRight, Map<Integer, Integer> index) {
        // case: empty node
        if (pLeft == pRight) return null;

        // 1. preorder[pLeft] is the root node
        TreeNode root = new TreeNode(preorder[pLeft]);

        // 2. locate the left & right subtree range
        int rootIndex = index.get(root.val);    // left: inorder[iLeft, rootIndex); right: inorder[rootIndex+1, iRight)
        int leftTotal = rootIndex - iLeft;      // left: preorder[pLeft+1, pLeft+1+leftTotal); right: preorder[pLeft+1+leftTotal, pRight)

        root.left = dfs(preorder, pLeft+1, pLeft+1+leftTotal, inorder, iLeft, rootIndex, index);
        root.right = dfs(preorder, pLeft+1+leftTotal, pRight, inorder, rootIndex+1, iRight, index);
        return root;
    }
}