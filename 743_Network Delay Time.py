class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        # Key Insight: find the furthest node distance from k -> Dijkstra
        # 1. build adj matrix (graph)
        adj = [[inf] * n for _ in range(n)] # row: from, col: to
        for u, v, w in times:
            adj[u-1][v-1] = w
        
        # 2. loop to find the furthest distance
        # A. init Dijkstra w/ distance (start = 0) & bool_done
        distance = [inf] * n
        done = [False] * n
        prev = distance[k-1] = 0    # prev is the distance of the last done node

        while True:
            curn = -1
            # B. loop to find undone shortest distance
            for i, d in enumerate(done):
                if (not d) and (curn == -1 or distance[i] < distance[curn]): curn = i
            
            # C. End Case: all done || unreacheable
            if curn == -1: return prev
            if distance[curn] == inf: return -1

            # D. mark as done & record its distance
            done[curn] = True
            prev = distance[curn]

            # E. explore its neighbors
            for v, d in enumerate(adj[curn]):
                distance[v] = min(distance[v], prev + d)