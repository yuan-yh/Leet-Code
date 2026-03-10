// 时间复杂度：O(n)，其中 n 是 nums 的长度。每次递归要么返回空节点，要么把 nums 的一个数转成一个节点，所以递归次数是 O(n) 的，所以时间复杂度是 O(n)。
// 空间复杂度：O(n)。如果不计入返回值和切片的空间，那么空间复杂度为 O(logn)，即递归栈的开销。

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
    private int[] nums;

    private TreeNode buildBST(int left, int right) {
        // 0. end case
        if (left > right) return null;

        // 1. middle as root
        int mid = left + (right - left) / 2;
        TreeNode root = new TreeNode(nums[mid]);

        // 2. left part build the left-subtree; right for right sub-tree
        TreeNode ltree = this.buildBST(left, mid-1);
        TreeNode rtree = this.buildBST(mid+1, right);

        root.left = ltree;
        root.right = rtree;
        return root;
    }

    public TreeNode sortedArrayToBST(int[] nums) {
        this.nums = nums;
        return this.buildBST(0, nums.length - 1);
    }
}