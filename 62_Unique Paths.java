class Solution {
    public int uniquePaths(int m, int n) {
        int row[] = new int[n];
        // init
        for (int i = 0; i < n; i++) row[i] = 1;
        // process
        for (int r = 1; r < m; r++) {
            for (int c = 1; c < n; c++) {
                row[c] += row[c-1];
            }
        }
        return row[n-1];
    }
}