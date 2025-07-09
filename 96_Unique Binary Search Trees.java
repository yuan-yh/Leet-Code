class Solution {
    public int numTrees(int n) {
        // edge end case
        if (n <= 2) return n;

        // case 0: zero node -> one tree structure
        // case 1: one node -> one tree structure
        // case 2: two nodes -> two tree structures
        // Therefore, reasoning: for future trees, count nodes for left / right subtrees

        // count[i] is the number of unique tree structures with i nodes
        int[] count = new int[n+1];
        // init
        count[0] = 1;
        count[1] = 1;
        count[2] = 2;

        for (int i = 3; i <= n; i++) {
            int tmp = 0;
            for (int root = 1; root <= i; root++) {
                int leftN = root - 1, rightN = i - root;
                tmp += count[leftN] * count[rightN];
            }
            count[i] = tmp;
        }
        return count[n];
    }
}