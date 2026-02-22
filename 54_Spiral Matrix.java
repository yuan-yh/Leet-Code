// 时间复杂度：O(mn)，其中 m 和 n 分别为 matrix 的行数和列数。
// 空间复杂度：O(1)。返回值不计入。

class Solution {
    public List<Integer> spiralOrder(int[][] matrix) {
        int[][] dir = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};
        List<Integer> res = new ArrayList<>();
        int row = matrix.length, col = matrix[0].length, r = 0, c = 0, d = 0;

        for (int i = 0; i < row*col; i++) {
            // 1. record & update visited
            res.add(matrix[r][c]);
            matrix[r][c] = -101;
            // 2. shift to the next valid position
            int nextr = r + dir[d][0], nextc = c + dir[d][1];
            // 3. turn 90D clockwise if out of boundary or visited
            if (nextr < 0 || nextr >= row || nextc < 0 || nextc >= col || matrix[nextr][nextc] == -101) {
                d = (d+1)%4;
            }
            r = r + dir[d][0];
            c = c + dir[d][1];
        }

        return res;
    }
}