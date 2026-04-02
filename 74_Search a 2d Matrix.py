# Method 1
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

# Method 2
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        # For each row, ASC; For each column, ASC; Next_Row > Cur_row
        # 1. start from diagonally (top-right or bottom-left)
        row, col = len(matrix), len(matrix[0])
        
        # 2. binary search rows in [lr, rr]
        lr, rr = 0, row - 1
        while lr < rr:
            mr = (lr + rr) >> 1
            if matrix[mr][col - 1] < target: lr = mr + 1
            elif matrix[mr][col - 1] > target: rr = mr
            else: return True
        
        # 3. binary search column in [lc, rc]
        lc, rc = 0, col - 1
        while lc < rc:
            mc = (lc + rc) >> 1
            if matrix[lr][mc] < target: lc = mc + 1
            elif matrix[lr][mc] > target: rc = mc - 1
            else: return True
        
        return matrix[lr][lc] == target