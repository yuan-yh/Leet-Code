// Time complexity: O(n^2)
// Space complexity: O(n^2)

class Solution {
    private int[][] map;
    private int[][] dir = {{-1, 0}, {0, 1}, {1, 0}, {0, -1}};
    private Queue<int[]> q;

    public int shortestBridge(int[][] grid) {
        this.map = grid;
        this.q = new LinkedList<>();
        int row = map.length, col = map[0].length;
        boolean foundFirstIsland = false;

        // 1. dfs - find the first island
        for (int r = 0; r < row; r++) {
            if (foundFirstIsland) break;
            for (int c = 0; c < col; c++) {
                if (map[r][c] == 1) {
                    dfs(r, c);
                    foundFirstIsland = true;
                    break;
                }
            }
        }

        // 2. bfs - explore surroundings
        int res = 0;
        while (!q.isEmpty()) {
            int size = q.size();
            for (int i = 0; i < size; i++) {
                int[] cur = q.poll();
                
                for (int[] d : dir) {
                    int curR = cur[0] + d[0];
                    int curC = cur[1] + d[1];

                    if (curR < 0 || curR >= row || curC < 0 || curC >= col) continue;

                    // 3. if spot '1' -> find the second island
                    if (map[curR][curC] == 1) return res;

                    if (map[curR][curC] == 0) {
                        map[curR][curC] = 2;
                        q.offer(new int[]{curR, curC});
                    }
                }
            }
            res++;
        }
        return res;
    }

    private void dfs(int curRow, int curCol) {
        // check boundary & water area
        if (curRow < 0 || curRow >= map.length || curCol < 0 || curCol >= map[0].length || map[curRow][curCol] != 1) return;

        // mark as visited - 2
        map[curRow][curCol] = 2;
        q.offer(new int[]{curRow, curCol});

        // explore surroundings
        for (int[] d : dir) dfs(curRow + d[0], curCol + d[1]);
    }
}