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
                    res = Math.max(res, bfs(grid, r, c));
                }
            }
        }

        return res;
    }

    private int bfs(int[][] grid, int curRow, int curCol) {
        Queue<int[]> q = new LinkedList<>();
        q.add(new int[]{curRow, curCol});
        grid[curRow][curCol] = 0;
        int area = 0, row = grid.length, col = grid[0].length;

        while (!q.isEmpty()) {
            int[] cur = q.poll();
            area++;

            for (int[] d : dir) {
                int tmpRow = cur[0] + d[0];
                int tmpCol = cur[1] + d[1];

                if (tmpRow < 0 || tmpRow >= row || tmpCol < 0 || tmpCol >= col || grid[tmpRow][tmpCol] == 0) continue;
                q.add(new int[]{tmpRow, tmpCol});
                grid[tmpRow][tmpCol] = 0;
            }
        }

        return area;
    }
}