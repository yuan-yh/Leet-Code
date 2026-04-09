class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        # Key Insight: 多源 BFS, similar to LC286
        # 1. count fresh & record rotten location
        fresh, row, col = 0, len(grid), len(grid[0])
        q = deque()

        for r in range(row):
            for c in range(col):
                if grid[r][c] == 1: fresh += 1
                elif grid[r][c] == 2: q.append((r, c))
        
        if fresh == 0: return 0

        # 2. 多源 BFS
        res = 0
        dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        while fresh > 0 and q:
            res += 1
            clen = len(q)
            for _ in range(clen):
                tr, tc = q.popleft()
                for dr, dc in dirs:
                    if 0 <= tr + dr < row and 0 <= tc + dc < col and grid[tr+dr][tc+dc] == 1:
                        grid[tr+dr][tc+dc] = 2
                        fresh -= 1
                        q.append((tr+dr, tc+dc))
            
        return res if fresh == 0 else -1