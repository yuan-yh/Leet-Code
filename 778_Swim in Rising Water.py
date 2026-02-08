class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        # Key: minimize the max height along the path -> Dijkstra
        # 1. init time records w/ the starting as grid[0][0]
        row, col = len(grid), len(grid[0])
        time = [[inf] * col for _ in range(row)]
        time[0][0] = grid[0][0]

        # 2. heap - help pick the quickest accessible spot
        heap = [(time[0][0], 0, 0)]     # (time, row, col)

        # 3. explore the cur neighbors
        while heap:
            curt, curr, curc = heappop(heap)
            if curr == row-1 and curc == col-1: return curt # the first reach must be the quickest approach
            if curt > time[curr][curc]: continue    # we may find a quicker path later so skip for now

            for nextr, nextc in (curr-1, curc), (curr, curc-1), (curr, curc+1), (curr+1, curc):
                if 0 <= nextr < row and 0 <= nextc < col:
                    nextt = max(grid[nextr][nextc], curt)
                    if nextt < time[nextr][nextc]:
                        time[nextr][nextc] = nextt
                        heappush(heap, (nextt, nextr, nextc))

        return time[-1][-1]