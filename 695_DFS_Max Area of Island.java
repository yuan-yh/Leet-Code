// Time complexity: O(m∗n)
// Space complexity: O(m∗n)
// Where m is the number of rows and n is the number of columns in the grid.

class Solution {
    private int[][] dir = {{-1, 0}, {0, 1}, {1, 0}, {0, -1}};

    public int maxAreaOfIsland(int[][] grid) {
        int row = grid.length, col = grid[0].length, res = 0;

        for (int r = 0; r < row; r++) {
            for (int c = 0; c < col; c++) {
                if (grid[r][c] == 1) {
                    res = Math.max(res, dfs(grid, r, c, row, col));
                }
            }
        }

        return res;
    }

    private int dfs(int[][] grid, int curRow, int curCol, int row, int col) {
        int area = 1;
        grid[curRow][curCol] = 0;

        for (int[] d : dir) {
            int tmpRow = curRow + d[0];
            int tmpCol = curCol + d[1];

            if (tmpRow < 0 || tmpRow >= row || tmpCol < 0 || tmpCol >= col || grid[tmpRow][tmpCol] == 0) continue;
            area += dfs(grid, tmpRow, tmpCol, row, col);
        }

        return area;
    }
}