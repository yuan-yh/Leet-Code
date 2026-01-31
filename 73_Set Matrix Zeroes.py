class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        # Space: O(1)
        # use the 1st row/col to record zerofy cases, while O(1) constants to record zerofy cases for the 1st roww/col themselves.
        row, col = len(matrix), len(matrix[0])
        # 1. record the 1st row / col
        zero_r1 = 0 in matrix[0]
        zero_c1 = any(matrix[r][0] == 0 for r in range(row))

        # 2. loop 1: for m[r][c] = 0, zerofy m[r][0] and m[0][c]
        for r in range(1, row):
            for c in range(1, col):
                if matrix[r][c] == 0: matrix[r][0] = matrix[0][c] = 0
        # 3. loop 2: zerofy based on m[r][0] and m[0][c]
        for r in range(1, row):
            for c in range(1, col):
                if matrix[r][0] == 0 or matrix[0][c] == 0: matrix[r][c] = 0
        # 4. zerofy the 1st row/col if necessary
        if zero_r1: matrix[0] = [0] * col
        if zero_c1: 
            for r in range(row): matrix[r][0] = 0

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