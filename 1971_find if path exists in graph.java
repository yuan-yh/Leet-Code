// Let n be the number of nodes and m be the number of edges.

// Time complexity: O(m⋅α(n))
// The amortized complexity for performing m union find operations is O(m⋅α(n)) time where α is the Inverse Ackermann Function.
// To sum up, the overall time complexity is O(m⋅α(n)).
// Space complexity: O(n)

class Solution {
    private int[] root;

    public boolean validPath(int n, int[][] edges, int source, int destination) {
        // Disjoint Set Union

        // 1. init with each vertext self-pointing
        root = new int[n];
        for (int i = 0; i < n; i++) root[i] = i;

        // 2. update the root by joining each edge
        for (int[] e : edges) join(e[0], e[1]);

        // 3. find the root vertext for each vertex
        return (find(source) == find (destination));
    }

    private void join(int v1, int v2) {
        int root1 = find(v1), root2 = find(v2);
        if (root1 != root2) root[root1] = root2;
    }

    private int find(int vertex) {
        int tmp = root[vertex];
        if (tmp != vertex) root[vertex] = find(tmp);
        return root[vertex];
    }
}