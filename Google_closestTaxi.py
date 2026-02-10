# See LC 994
from collections import deque

def shortest_distance_to_taxi(matrix):
    m, n = len(matrix), len(matrix[0])
    dist = [[-1] * n for _ in range(m)]
    queue = deque()

    # 把所有 taxi 作为源点入队
    for i in range(m):
        for j in range(n):
            if matrix[i][j] == 'taxi':
                queue.append((i, j))
                dist[i][j] = 0

    # BFS 扩展
    directions = [(0,1),(0,-1),(1,0),(-1,0)]
    while queue:
        x, y = queue.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < m and 0 <= ny < n and dist[nx][ny] == -1:
                dist[nx][ny] = dist[x][y] + 1
                queue.append((nx, ny))

    return dist

# Follow-up: taxi 会随时上线或下线，你需要设计一个系统，能随时回答"某个 cell 到最近的在线 taxi 的距离是多少？
# 第一步：每个 taxi 上线时，单独做一次 BFS
# 第二步：每个 cell 维护一个 min-heap
# 第三步：维护一个 online_set 记录在线状态
# 第四步：查询时用 Lazy Deletion

# 初始化：每个 cell 一个空 list（之后当 min-heap 用）
heaps = [[[] for _ in range(col)] for _ in range(row)]

import heapq
# 空间复杂度是 O(m × n × k)，其中 k 是历史 taxi 总数
def taxi_online(taxi_id, taxi_pos, heaps, online_set):
    online_set.add(taxi_id)
    
    # BFS 算出这个 taxi 到每个 cell 的距离
    dist = bfs(taxi_pos)  
    
    # 把结果 push 进每个 cell 的 heap
    for i in range(row):
        for j in range(col):
            heapq.heappush(heaps[i][j], (dist[i][j], taxi_id))