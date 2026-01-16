class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        row, col = len(matrix), len(matrix[0])
        # 1. diagonal reflection (right downwards)
        for r in range(row):
            for c in range(r + 1):
                matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]
        # 2. mirror image: row reflection
        for r in range(row):
            left, right = 0, col - 1
            while left < right:
                matrix[r][left], matrix[r][right] = matrix[r][right], matrix[r][left]
                left += 1
                right -= 1