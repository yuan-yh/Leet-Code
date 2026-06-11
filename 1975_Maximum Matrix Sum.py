class Solution:
    def maxMatrixSum(self, matrix: List[List[int]]) -> int:
        # Even Negative: all processed
        # Odd Negative: remain the smallest one if no zero, otherwise like even
        n = len(matrix)
        res, zero, negCnt, minVal = 0, False, 0, inf

        for r in range(n):
            for c in range(n):
                if matrix[r][c] == 0: zero = True
                elif matrix[r][c] < 0: negCnt += 1
                res += abs(matrix[r][c])
                minVal = min(abs(minVal), abs(matrix[r][c]))
        
        if not zero and negCnt % 2 == 1: res -= 2*abs(minVal)

        return res