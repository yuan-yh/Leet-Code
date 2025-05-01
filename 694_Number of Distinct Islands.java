// Hash By Path Signature
// Time Complexity: O(M⋅N)
// Space Complexity: O(M⋅N)

class Solution {
    private int[][] map;
    private Set<String> shapeSet;

    public int numDistinctIslands(int[][] grid) {
        this.map = grid;
        this.shapeSet = new HashSet<>();

        StringBuilder sb;
        int row = grid.length, col = grid[0].length;

        // explore an island & record its shape
        for (int r = 0; r < row; r++) {
            for (int c = 0; c < col; c++) {
                if (grid[r][c] == 1) {
                    sb = new StringBuilder();
                    dfs(r, c, sb, '0');
                    if (sb.length() > 0) this.shapeSet.add(sb.toString());
                }
            }
        }

        return this.shapeSet.size();
    }

    private void dfs(int curRow, int curCol, StringBuilder sb, Character dir) {
        int row = map.length, col = map[0].length;
        // check for boundary or water area
        if (curRow < 0 || curRow >= row || curCol < 0 || curCol >= col || map[curRow][curCol] == 0) return;
        
        // mark as visited
        map[curRow][curCol] = 0;
        sb.append(dir);

        // record shape (up / right / down / left)
        dfs(curRow-1, curCol, sb, 'U');
        dfs(curRow, curCol+1, sb, 'R');
        dfs(curRow+1, curCol, sb, 'D');
        dfs(curRow, curCol-1, sb, 'L');

        sb.append('0');
    }
}