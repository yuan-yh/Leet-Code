# Method 1: 多源 BFS
class Solution:
    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        """
        Do not return anything, modify rooms in-place instead.
        """
        # Key Insight: 多源 BFS, similar to LC994
        # 1. enque gates
        row, col = len(rooms), len(rooms[0])
        q = deque()
        for r in range(row):
            for c in range(col):
                if rooms[r][c] == 0: q.append((r, c))
        
        # 2. step loop simulation: explore neighbors w/in 1 step
        step = 0
        while q:
            step += 1
            curL = len(q)

            for _ in range(curL):
                curr, curc = q.popleft()
                for nextr, nextc in (curr-1, curc), (curr, curc-1), (curr, curc+1), (curr+1, curc):
                    if 0 <= nextr < row and 0 <= nextc < col and rooms[nextr][nextc] == 2147483647:
                        # mark the room at the current step
                        # No need to worry smaller step_cnt from other gates in this case
                        rooms[nextr][nextc] = step
                        q.append((nextr, nextc))

# # Method 2: BFS
# class Solution:
#     def wallsAndGates(self, rooms: List[List[int]]) -> None:
#         """
#         Do not return anything, modify rooms in-place instead.
#         """
#         # BFS: first push all gates into queue, then explore its surroundings
#         reach = deque()
#         row, col = len(rooms), len(rooms[0])
#         directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

#         # 1. find all gates
#         for r in range(row):
#             for c in range(col):
#                 if rooms[r][c] == 0: reach.append((r, c))
        
#         # 2. for each reachable spot, explore it surroundings: terminate explore the cur spot if gate/wall/record<from cur path
#         while reach:
#             curR, curC = reach.popleft()
#             for dr, dc in directions:
#                 nextR, nextC = curR + dr, curC + dc
#                 if 0 <= nextR < row and 0 <= nextC < col and rooms[nextR][nextC] > rooms[curR][curC] + 1:
#                     rooms[nextR][nextC] = rooms[curR][curC] + 1
#                     reach.append((nextR, nextC))