class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        # Binary Search based on idx
        row, col = len(matrix), len(matrix[0])
        left, right = 0, row*col - 1

        while left <= right:
            mid = left + ((right - left) >> 1)
            mrow = mid // col
            mcol = mid % col

            if matrix[mrow][mcol] == target: return True
            elif matrix[mrow][mcol] < target: left = mid + 1
            else: right = mid - 1

        return False