// 时间复杂度：O(m+n)，其中 m 和 n 分别为 matrix 的行数和列数。每次循环排除掉一行或者一列，一共 m+n 行列，最坏情况下需要排除 m+n−1 行列才能找到答案。
// 空间复杂度：O(1)。

class Solution {
    public boolean searchMatrix(int[][] matrix, int target) {
        // 1. start from bottom-left corner (or top-right)
        int row = matrix.length, col = matrix[0].length;
        int r = row - 1, c = 0;

        while (r >= 0 && c < col) {
            if (matrix[r][c] == target) return true;
            // case: cur > target, then this row must not exists target -> shift upwards
            else if (matrix[r][c] > target) r -= 1;
            // case: cur < target, then target must not in this column -> shift rightwards
            else c += 1;
        }

        return false;
    }
}