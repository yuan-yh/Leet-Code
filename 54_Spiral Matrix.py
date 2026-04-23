# 螺旋结构确保当你撞到墙壁或访问过的牢房并顺时针转90°时，新路径是开放的

class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        res = []
        row, col = len(matrix), len(matrix[0])
        r = c = d = 0

        for _ in range(row*col):
            # update res
            res.append(matrix[r][c])
            # mark as visited
            matrix[r][c] = -inf
            # explore the next valid position
            if not (0 <= r + dirs[d][0] < row and 0 <= c + dirs[d][1] < col and matrix[r+dirs[d][0]][c+dirs[d][1]] != -inf): d = (d + 1) % 4
            r, c = r + dirs[d][0], c + dirs[d][1]
        return res