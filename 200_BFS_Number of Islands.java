// Time complexity: O(m∗n)
// Space complexity: O(m∗n)

class Solution {
    private int[][] dir = {{-1, 0}, {0, 1}, {1, 0}, {0, -1}};

    public int numIslands(char[][] grid) {
        int row = grid.length, col = grid[0].length, count = 0;
        for (int r = 0; r < row; r++) {
            for (int c = 0; c < col; c++) {
                if (grid[r][c] == '1') {
                    count ++;
                    bfs(grid, r, c, row, col);
                }
            }
        }
        return count;
    }

    private void bfs(char[][] grid, int curRow, int curCol, int row, int col) {
        Queue<int[]> q = new LinkedList<>();
        grid[curRow][curCol] = '0';
        q.add(new int[]{curRow, curCol});

        while (!q.isEmpty()) {
            int[] tmp = q.poll();
            for (int[] d : dir) {
                int newRow = tmp[0] + d[0];
                int newCol = tmp[1] + d[1];

                if (newRow < 0 || newRow >= row || newCol < 0 || newCol >= col || grid[newRow][newCol] == '0') continue;
                grid[newRow][newCol] = '0';
                q.add(new int[]{newRow, newCol});
            }
        }
    }
}