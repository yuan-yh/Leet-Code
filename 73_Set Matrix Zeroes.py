class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        # Space: O(m+n)
        # 1. loop to collect target row/col
        row, col = len(matrix), len(matrix[0])
        r0, c0 = set(), set()
        for r in range(row):
            for c in range(col):
                if matrix[r][c] == 0:
                    r0.add(r)
                    c0.add(c)
        # 2. set to 0s
        for r in range(row):
            for c in range(col):
                if r in r0 or c in c0:
                    matrix[r][c] = 0