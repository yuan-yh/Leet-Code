// 时间复杂度：O(mn)，其中 m 和 n 分别是 matrix 的行数和列数。
// 空间复杂度：O(1)。

class Solution {
    public void setZeroes(int[][] matrix) {
        boolean firstRow0 = false, firstCol0 = false;
        int row = matrix.length, col = matrix[0].length;

        // 1. record if zero the first col / row
        for (int r = 0; r < row; r++) {
            if (matrix[r][0] == 0) {
                firstCol0 = true;
                break;
            }
        }
        for (int c = 0; c < col; c++) {
            if (matrix[0][c] == 0) {
                firstRow0 = true;
                break;
            }
        }
        // 2. record the inner matrix in the 1st row/col
        for (int r = 1; r < row; r++) {
            for (int c = 1; c < col; c++) {
                if (matrix[r][c] == 0) {
                    matrix[0][c] = 0;
                    matrix[r][0] = 0;
                }
            }
        }
        // 3. update the inner matrix
        for (int r = 1; r < row; r++) {
            for (int c = 1; c < col; c++) {
                if (matrix[0][c] == 0 || matrix[r][0] == 0) matrix[r][c] = 0;
            }
        }
        // 4. update the 1st row / col
        if (firstRow0) {
            for (int c = 0; c < col; c++) matrix[0][c] = 0;
        }
        if (firstCol0) {
            for (int r = 0; r < row; r++) matrix[r][0] = 0;
        }
    }
}