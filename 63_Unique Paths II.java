class Solution {
    public int uniquePathsWithObstacles(int[][] obstacleGrid) {
        int row = obstacleGrid.length, col = obstacleGrid[0].length;
        // edge case
        if (obstacleGrid[0][0] == 1 || obstacleGrid[row-1][col-1] == 1) return 0;
        // init
        int[] rowTmp = new int[col];
        rowTmp[0] = 1;
        for (int i = 1; i < col; i++) {
            if (obstacleGrid[0][i] == 0) rowTmp[i] = rowTmp[i-1];
        }
        // process
        for (int r = 1; r < row; r++) {
            for (int c = 0; c < col; c++) {
                rowTmp[c] = (obstacleGrid[r][c] == 1) ? 0 : (c == 0 ? rowTmp[c] : rowTmp[c] + rowTmp[c-1]);
            }
        }
        return rowTmp[col - 1];
    }
}