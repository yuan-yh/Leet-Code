class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        # Key: minimize the max height along the path -> Dijkstra
        # 1. init time record w/ the start as grid[0][0]
        row, col = len(grid), len(grid[0])
        time = [[inf] * col for _ in range(row)]
        time[0][0] = grid[0][0]

        # 2. build min-heap (time, row, col)
        heap = [(time[0][0], 0, 0)]

        # 3. explore neighbors of the quickest accessible spot
        while heap:
            curt, curr, curc = heappop(heap)
            # 4. short-cut: first reach to end must be the fastest
            if curr == row-1 and curc == col-1: return curt
            # 5. short-cut: avoid faster records which being pushed later but processed earlier already
            if curt > time[curr][curc]: continue
            # 6. explore neighbors: update and push inito heap if faster
            for nextr, nextc in (curr-1, curc), (curr, curc-1), (curr, curc+1), (curr+1, curc):
                if 0 <= nextr < row and 0 <= nextc < col:
                    nextt = max(grid[nextr][nextc], curt)
                    if nextt < time[nextr][nextc]:
                        time[nextr][nextc] = nextt
                        heappush(heap, (nextt, nextr, nextc))

        return time[-1][-1]