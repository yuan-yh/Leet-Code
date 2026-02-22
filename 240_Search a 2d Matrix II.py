class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        """
        1. For ASC in cols, shift leftwards when cur > target
        2. For ASC in rows, shift downwards when cur < target
        """
        row, col = len(matrix), len(matrix[0])
        r, c = 0, col-1

        while r < row and c >= 0:
            if matrix[r][c] == target: return True
            # 这一行剩余元素全部小于 target，排除
            elif matrix[r][c] < target: r += 1
            # 这一列剩余元素全部大于 target，排除
            else: c -= 1
        return False