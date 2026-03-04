// 时间复杂度：O(n)，其中 n 为二叉树的节点个数。虽然写了个二重循环，但每个节点只会入队出队各一次，所以总的循环次数是节点个数之和，即 O(n)。
// 空间复杂度：O(n)。满二叉树（每一层都填满）最后一层有大约 n/2 个节点，因此队列中最多有 O(n) 个元素，所以空间复杂度是 O(n) 的。


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
    public List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> res = new ArrayList<>();
        Deque<TreeNode> q = new LinkedList<>();
        if (root != null) q.offer(root);

        while (!q.isEmpty()) {
            List<Integer> cur = new ArrayList<>();
            int size = q.size();

            for (int i = 0; i < size; i++) {
                TreeNode tmp = q.poll();
                cur.add(tmp.val);
                if (tmp.left != null) q.offer(tmp.left);
                if (tmp.right != null) q.offer(tmp.right);
            }
            res.add(cur);
        }

        return res;
    }
}