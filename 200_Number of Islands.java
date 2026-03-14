// Time complexity: O(m∗n)
// Space complexity: O(m∗n)

class Solution {
    private char[][] grid;
    private int[][] dir = {{-1, 0}, {0, 1}, {1, 0}, {0, -1}};

    private void dfs(int curR, int curC, int row, int col) {
        if (curR < 0 || curR >= row || curC < 0 || curC >= col || this.grid[curR][curC] != '1') return;

        this.grid[curR][curC] = '0';
        dfs(curR-1, curC, row, col);
        dfs(curR+1, curC, row, col);
        dfs(curR, curC+1, row, col);
        dfs(curR, curC-1, row, col);
    }

    private void bfs(int curR, int curC, int row, int col) {
        Queue<int[]> q = new LinkedList<>();
        q.offer(new int[]{curR, curC});
        this.grid[curR][curC] = '0';

        while (!q.isEmpty()) {
            int[] tmp = q.poll();
            for (int[] d : dir) {
                int newR = tmp[0] + d[0], newC = tmp[1] + d[1];

                if (newR >= 0 && newR < row && newC >= 0 && newC < col && this.grid[newR][newC] == '1') {
                    this.grid[newR][newC] = '0';
                    q.offer(new int[]{newR, newC});
                }
            }
        }
    }

    public int numIslands(char[][] grid) {
        this.grid = grid;
        int row = grid.length, col = grid[0].length, cnt = 0;

        for (int r = 0; r < row; r++) {
            for (int c = 0; c < col; c++) {
                if (this.grid[r][c] == '1') {
                    // bfs(r, c, row, col);
                    dfs(r, c, row, col);
                    cnt += 1;
                }
            }
        }
        return cnt;
    }
}