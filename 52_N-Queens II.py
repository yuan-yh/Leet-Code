class Solution:
    def totalNQueens(self, n: int) -> int:
        def dfs(curRow):
            # end case
            if curRow == n:
                nonlocal res
                res += 1
                return
            # process
            for c in range(n):
                if not(colb[c] or diagP[curRow+c] or diagN[curRow-c+n-1]):
                    colb[c] = diagP[curRow+c] = diagN[curRow-c+n-1] = True
                    dfs(curRow + 1)
                    colb[c] = diagP[curRow+c] = diagN[curRow-c+n-1] = False
        
        # 1. init visit records
        colb = [False] * n
        # For grids along the same positive diagonal, r+c - constant
        # For grids along the same negative diagonal, r-c+(n-1) - constant
        diagP, diagN = [False] * (2*n - 1), [False] * (2*n - 1)
        # 2. dfs
        res = 0
        dfs(0)
        return res