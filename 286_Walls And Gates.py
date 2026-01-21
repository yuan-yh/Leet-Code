class Solution:
    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        """
        Do not return anything, modify rooms in-place instead.
        """
        # BFS: first push all gates into queue, then explore its surroundings
        reach = deque()
        row, col = len(rooms), len(rooms[0])
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        # 1. find all gates
        for r in range(row):
            for c in range(col):
                if rooms[r][c] == 0: reach.append((r, c))
        
        # 2. for each reachable spot, explore it surroundings: terminate explore the cur spot if gate/wall/record<from cur path
        while reach:
            curR, curC = reach.popleft()
            for dr, dc in directions:
                nextR, nextC = curR + dr, curC + dc
                if 0 <= nextR < row and 0 <= nextC < col and rooms[nextR][nextC] > rooms[curR][curC] + 1:
                    rooms[nextR][nextC] = rooms[curR][curC] + 1
                    reach.append((nextR, nextC))