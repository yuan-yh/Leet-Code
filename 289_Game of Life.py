class Solution:
    def gameOfLife(self, board: List[List[int]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        # Bit Manipulation: update to 1(next)0(prev)
        # &1 to extract the last bit, >>= to discard
        row, col = len(board), len(board[0])

        def countLN(curR, curC) -> int:
            cnt = 0
            d = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

            for dr, dc in d:
                nr, nc = curR + dr, curC + dc
                if 0 <= nr < row and 0 <= nc < col: cnt += board[nr][nc] & 1
            return cnt

        # 1. update board[r][c]'s 2nd bit based on ln
        for r in range(row):
            for c in range(col):
                cnt = countLN(r, c)
                # live case 1: live with 2-3 live neighbors
                if board[r][c] == 1 and 2 <= cnt <= 3: board[r][c] = 3  #Bit: 11
                # live case 2: dead with 3 live neighbors
                if board[r][c] == 0 and cnt == 3: board[r][c] = 2       #Bit: 10
        
        # 2. update board by discarding the last bit
        for r in range(row):
            for c in range(col):
                board[r][c] >>= 1