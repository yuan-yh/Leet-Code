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

// Breadth First Search (Optimal)
// Time complexity: O(n)
// Space complexity: O(n)

class Solution {
    public List<List<Integer>> verticalOrder(TreeNode root) {
        if (root == null) return new ArrayList<>();

        // column - List<Node values>
        Map<Integer, List<Integer>> m = new HashMap<>();
        // Pair<Node, column>
        Queue<Pair<TreeNode, Integer>> q = new LinkedList<>();

        q.add(new Pair<>(root, 0));
        int minCol = 0, maxCol = 0;

        while (!q.isEmpty()) {
            Pair<TreeNode, Integer> p = q.poll();
            TreeNode curNode = p.getKey();
            int curCol = p.getValue();

            // record in hashmap, update min/maxCol
            m.putIfAbsent(curCol, new ArrayList<>());
            m.get(curCol).add(curNode.val);
            minCol = Math.min(minCol, curCol);
            maxCol = Math.max(maxCol, curCol);

            if (curNode.left != null) q.add(new Pair<>(curNode.left, curCol - 1));
            if (curNode.right != null) q.add(new Pair<>(curNode.right, curCol + 1));
        }

        List<List<Integer>> res = new ArrayList<>();
        for (int i = minCol; i <= maxCol; i++) {
            res.add(m.get(i));
        }
        return res;
    }
}

// Depth First Search (Optimal)
// Time complexity: O(w∗hlogh)
// Space complexity: O(n)
// Where n is the number of nodes, h is the height of the tree (i.e. maximum number of nodes in any vertical line of the tree), and w is the width of the tree (i.e. maximum number of nodes in any of the levels of the tree).

class Solution {
    // Column - List<int[]{row, node.val}>
    private Map<Integer, List<int[]>> m = new HashMap<>();
    private int minCol = 0, maxCol = 0;

    public List<List<Integer>> verticalOrder(TreeNode root) {
        if (root == null) return new ArrayList<>();

        dfs(root, 0, 0);

        List<List<Integer>> res = new ArrayList<>();
        for (int i = minCol; i <= maxCol; i++) {
            List<int[]> tmp = m.get(i);
            tmp.sort((a, b) -> (a[0] - b[0]));

            List<Integer> cur = new ArrayList<>();
            for (int[] t : tmp) cur.add(t[1]);
            res.add(cur);
        }
        return res;
    }

    private void dfs(TreeNode node, int col, int row) {
        minCol = Math.min(minCol, col);
        maxCol = Math.max(maxCol, col);
        m.putIfAbsent(col, new ArrayList<>());
        m.get(col).add(new int[]{row, node.val});

        if (node.left != null) dfs(node.left, col-1, row+1);
        if (node.right != null) dfs(node.right, col+1, row+1);
    }
}