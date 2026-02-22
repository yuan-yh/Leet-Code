// 时间复杂度：O(n^2 )，其中 n 是 matrix 的行数和列数
// 空间复杂度：O(1)

class Solution {
    public void rotate(int[][] matrix) {
        int row = matrix.length, col = matrix[0].length;

        // 1. reflect right-downwards diagnally
        for (int r = 1; r < row; r++) {
            for (int c = 0; c < r; c++) {
                int tmp = matrix[r][c];
                matrix[r][c] = matrix[c][r];
                matrix[c][r] = tmp;
            }
        }
        // 2. mirror lines
        for (int r = 0; r < row; r++) {
            int left = 0, right = col - 1;
            while (left < right) {
                int tmp = matrix[r][left];
                matrix[r][left++] = matrix[r][right];
                matrix[r][right--] = tmp;
            }
        }
    }
}