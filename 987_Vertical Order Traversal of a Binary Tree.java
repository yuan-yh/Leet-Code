// 时间复杂度：O(nlogn)，其中 n 为二叉树的节点个数。无论用何种方式遍历二叉树，基于比较的排序都需要 O(nlogn) 的时间
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
    private int minCol = 0;

    public List<List<Integer>> verticalTraversal(TreeNode root) {
        // 1. HashMap: key - column, val - int[]{row, node.val}
        Map<Integer, List<int[]>> record = new HashMap<>();
        // 2. Traversal: record col & row for each node
        dfs(root, 0, 0, record);
        // 3. Sort col (left -> right) / row (top -> bottom) / val (ASC)
        List<List<Integer>> res = new ArrayList<>();

        for (int i = minCol; i < minCol + record.size(); i++) {
            List<int[]> tmp = record.get(i);
            tmp.sort((a, b) -> ((a[0] == b[0]) ? (a[1] - b[1]) : (b[0] - a[0])));

            List<Integer> r = new ArrayList<>();
            for (int[] t : tmp) r.add(t[1]);
            res.add(r);
        }

        return res;
    }

    private void dfs(TreeNode node, int row, int col, Map<Integer, List<int[]>> record) {
        if (node == null) return;

        List<int[]> tmp = record.getOrDefault(col, new ArrayList<>());
        tmp.add(new int[]{row, node.val});
        record.put(col, tmp);
        minCol = Math.min(minCol, col);

        dfs(node.left, row - 1, col - 1, record);
        dfs(node.right, row - 1, col + 1, record);
    }
}