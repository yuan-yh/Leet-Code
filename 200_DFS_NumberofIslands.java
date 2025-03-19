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
                    dfs(grid, r, c, row, col);
                }
            }
        }
        return count;
    }

    private void dfs(char[][] grid, int curRow, int curCol, int row, int col) {
        grid[curRow][curCol] = '0';
        for (int[] i : dir) {
            int newRow = curRow + i[0];
            int newCol = curCol + i[1];

            if (newRow < 0 || newRow >= row || newCol < 0 || newCol >= col || grid[newRow][newCol] == '0') continue;
            dfs(grid, newRow, newCol, row, col);
        }
    }
}