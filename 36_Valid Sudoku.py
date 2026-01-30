class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        cubes = [set() for _ in range(9)]

        for r in range(9):
            for c in range(9):
                cur = board[r][c]
                # 0. skip for empty fields
                if cur == ".": continue
                
                # 1. check for row / col / cubes
                # cubes are labelled left to right then up to down
                cIdx = (r // 3) * 3 + (c // 3)
                if cur in rows[r] or cur in cols[c] or cur in cubes[cIdx]: return False
                rows[r].add(cur)
                cols[c].add(cur)
                cubes[cIdx].add(cur)
        
        return True