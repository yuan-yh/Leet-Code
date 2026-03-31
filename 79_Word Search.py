class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        dirs = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        row, col = len(board), len(board[0])

        def dfs(curR, curC, idx) -> bool:
            # end case
            if curR < 0 or curR >= row or curC < 0 or curC >= col or board[curR][curC] != word[idx]: return False
            if idx == len(word) - 1: return True

            # process
            bt_mark = board[curR][curC]
            board[curR][curC] = '.'

            for dr, dc in dirs:
                if dfs(curR + dr, curC + dc, idx + 1): return True
            
            board[curR][curC] = bt_mark
            return False
        
        for r in range(row):
            for c in range(col):
                if dfs(r, c, 0): return True
        return False