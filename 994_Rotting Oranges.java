// Time complexity: O(m∗n)
// Space complexity: O(m∗n)
// Where m is the number of rows and n is the number of columns in the grid.

class Solution {
    private int[][] dir = {{-1, 0}, {0, 1}, {1, 0}, {0, -1}};

    public int orangesRotting(int[][] grid) {
        // BFS
        Queue<int[]> q = new LinkedList<>();
        int fresh = 0, time = 0, row = grid.length, col = grid[0].length;
        // 1. push original-rotten orange into the queue
        for (int r = 0; r < row; r++) {
            for (int c = 0; c < col; c++) {
                if (grid[r][c] == 1) fresh++;
                else if (grid[r][c] == 2) q.add(new int[]{r, c});
            }
        }
        // 2. infect adjacent oranges like infect next for orig-rot -> infeect next for 1st-gen rot
        // fresh>0 to cut the process when no fresh orange left
        while (fresh > 0 && !q.isEmpty()) {
            int length = q.size();
            for (int i = 0; i < length; i++) {
                int[] tmp = q.poll();
                for (int[] d : dir) {
                    int tmpRow = tmp[0] + d[0];
                    int tmpCol = tmp[1] + d[1];
                    if (tmpRow < 0 || tmpRow >= row || tmpCol < 0 || tmpCol >= col || grid[tmpRow][tmpCol] != 1) continue;
                    // infect the fresh orange
                    grid[tmpRow][tmpCol] = 2;
                    q.add(new int[]{tmpRow, tmpCol});
                    fresh--;
                }
            }
            time++;
        }
        return (fresh == 0) ? time : -1;
    }
}