// Time Complexity: O(n)
// Space Complexity: O(n)

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
    private int maxCount = 0;
    private Map<Integer, Integer> count = new HashMap<>();  // <tree_sum, count>

    private int dfs(TreeNode node) {
        if (node == null) return 0;

        int curSum = dfs(node.left) + dfs(node.right) + node.val;
        count.put(curSum, count.getOrDefault(curSum, 0) + 1);
        maxCount = Math.max(maxCount, count.get(curSum));
        return curSum;
    }

    public int[] findFrequentTreeSum(TreeNode root) {
        // calculate sum for all trees
        dfs(root);
        // collect sum with max counts
        List<Integer> tmp = new ArrayList<>();
        for (Map.Entry<Integer, Integer> e : count.entrySet()) {
            if (e.getValue() == maxCount) tmp.add(e.getKey());
        }
        int[] res = new int[tmp.size()];
        for (int i = 0; i < tmp.size(); i++) res[i] = tmp.get(i);
        return res;
    }
}