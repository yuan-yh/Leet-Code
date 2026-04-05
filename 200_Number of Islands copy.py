class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        row, col = len(grid), len(grid[0])
        dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        res = 0

        # DFS
        def dfs(curr: int, curc: int):
            # 1. mark as visited
            grid[curr][curc] = "0"
            # 2. explore surroundings
            for dr, dc in dirs:
                if 0 <= curr + dr < row and 0 <= curc + dc < col and grid[curr+dr][curc+dc] == "1":
                    dfs(curr + dr, curc + dc)
        
        # BFS
        def bfs(curr: int, curc: int):
            # 1. mark as visited
            grid[curr][curc] = "0"
            # 2. enque, explore, and mark before enque
            q = deque()
            q.append((curr, curc))
            while q:
                tr, tc = q.popleft()
                for dr, dc in dirs:
                    if 0 <= tr + dr < row and 0 <= tc + dc < col and grid[tr+dr][tc+dc] == "1":
                        grid[tr+dr][tc+dc] = "0"
                        q.append((tr + dr, tc + dc))
        
        for r in range(row):
            for c in range(col):
                if grid[r][c] == "1":
                    res += 1
                    # dfs(r, c)
                    bfs(r, c)
        return res
        
        