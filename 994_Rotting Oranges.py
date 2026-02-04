class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        # Key Insight: 多源 BFS, similar to LC286
        # 1. loop to count fresh & enque original rottens
        row, col, fresh = len(grid), len(grid[0]), 0
        rot = deque()

        for r in range(row):
            for c in range(col):
                if grid[r][c] == 1 :fresh += 1
                elif grid[r][c] == 2: rot.append((r, c))
        
        # 2. time loop simulation: infect fresh neighbors
        # End case: no fresh left or empty queue
        time = 0
        while rot and fresh > 0:
            time += 1
            curL = len(rot)

            for _ in range(curL):
                curr, curc = rot.popleft()
                for nextr, nextc in (curr-1, curc), (curr, curc-1), (curr, curc+1), (curr+1, curc):
                    if 0 <= nextr < row and 0 <= nextc < col and grid[nextr][nextc] == 1:
                        # infect fresh neighbors & enque
                        grid[nextr][nextc] = 2
                        rot.append((nextr, nextc))
                        fresh -= 1

        # 3. return based on left fresh count
        return -1 if fresh > 0 else time