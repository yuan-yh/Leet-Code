// Backtracking
// Time Complexity: O(2^N ⋅N)
// Space Complexity: O(N)

class Solution {
    List<Integer> path;
    List<List<Integer>> res;

    public List<List<Integer>> allPathsSourceTarget(int[][] graph) {
        path = new ArrayList<>();
        res = new ArrayList<>();
        dfs(graph, 0, graph.length - 1);
        return res;
    }

    private void dfs(int[][] graph, int start, int end) {
        path.add(start);
        if (start == end) {
            res.add(new ArrayList<>(path));
            return;
        }
        for (int v : graph[start]) {
            dfs(graph, v, end);
            path.remove(path.size() - 1);
        }
    }
}