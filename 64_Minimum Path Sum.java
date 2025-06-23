class Solution {
    public int minPathSum(int[][] grid) {
        int row = grid.length, col = grid[0].length;

        // init the first row & col
        for (int r = 1; r < row; r++) grid[r][0] += grid[r-1][0];
        for (int c = 1; c < col; c++) grid[0][c] += grid[0][c-1];

        // update the rest
        for (int r = 1; r < row; r++) {
            for (int c = 1; c < col; c++) {
                grid[r][c] += Math.min(grid[r-1][c], grid[r][c-1]);
            }
        }
        return grid[row-1][col-1];
    }
}