// 时间复杂度：O(log(mn))，其中 m 和 n 分别为 matrix 的行数和列数。
// 空间复杂度：O(1)。

class Solution {
    public boolean searchMatrix(int[][] matrix, int target) {
        // Binary Search based on the relative idx
        int row = matrix.length, col = matrix[0].length;
        int left = 0, right = row*col - 1;

        while (left <= right) {
            int mid = left + ((right - left) >> 1);
            int mrow = mid / col;
            int mcol = mid % col;

            if (matrix[mrow][mcol] == target) return true;
            else if (matrix[mrow][mcol] > target) right = mid-1;
            else left = mid+1;
        }

        return false;
    }
}