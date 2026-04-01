class Solution:
    def totalNQueens(self, n: int) -> int:
        def dfs(curRow: int):
            # end case
            if curRow == n:
                nonlocal res
                res += 1
                return
            # process
            for c in range(n):
                if not(colb[c] or diagP[curRow + c] or diagN[curRow - c + n - 1]):
                    colb[c] = diagP[curRow + c] = diagN[curRow - c + n - 1] = True
                    board[curRow][c] = 'Q'
                    dfs(curRow + 1)
                    board[curRow][c] = '.'
                    colb[c] = diagP[curRow + c] = diagN[curRow - c + n - 1] = False

        # 1. init visit records
        board = [['.'] * n for _ in range(n)]
        colb = [False] * n
        # For all grids along the same positive diagnoal, r+c - constant
        # For all grids along the same negative diagnoal, r-c+(n-1) - constant
        diagP, diagN = [False] * (2*n - 1), [False] * (2*n - 1)

        # 2. dfs
        res = 0
        dfs(0)
        return res