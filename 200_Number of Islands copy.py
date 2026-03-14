class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        row, col, cnt = len(grid), len(grid[0]), 0
        d = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        def dfs(curR, curC, row, col):
            grid[curR][curC] = '0'
            for dr, dc in d:
                if 0 <= curR + dr < row and 0 <= curC + dc < col and grid[curR + dr][curC + dc] == '1':
                    dfs(curR + dr, curC + dc, row, col)
        
        def bfs(curR, curC, row, col):
            q = deque()
            grid[curR][curC] = '0'
            q.append([curR, curC])

            while q:
                tr, tc = q.popleft()
                for dr, dc in d:
                    if 0 <= tr + dr < row and 0 <= tc + dc < col and grid[tr + dr][tc + dc] == '1':
                        grid[tr + dr][tc + dc] = '0'
                        q.append([tr + dr, tc + dc])

        for r in range(row):
            for c in range(col):
                if grid[r][c] == '1':
                    bfs(r, c, row, col)
                    # dfs(r, c, row, col)
                    cnt += 1
        return cnt