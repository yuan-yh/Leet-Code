# 螺旋结构确保当你撞到墙壁或访问过的牢房并顺时针转90°时，新路径是开放的

class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]     # clockwise
        row, col, i, j, d = len(matrix), len(matrix[0]), 0, 0, 0
        res = []

        for _ in range(row * col):
            # 1. record & mark as visited
            res.append(matrix[i][j])
            matrix[i][j] = None
            # 2. if out of boundary or visited, turn 90D clockwise
            nexti, nextj = i + directions[d][0], j + directions[d][1]
            if (not 0 <= nexti < row) or (not 0 <= nextj < col) or (matrix[nexti][nextj] == None):
                d = (d + 1) % 4
            i, j = i + directions[d][0], j + directions[d][1]

        return res