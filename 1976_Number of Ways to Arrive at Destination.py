class Solution:
    def countPaths(self, n: int, roads: List[List[int]]) -> int:
        # Key Insight: Dijkstra
        mod = 10**9 + 7
        # 1. build adj list
        adj = [[] for _ in range(n)]
        for u, v, t in roads:
            adj[u].append((v, t))
            adj[v].append((u, t))
        
        # 2. init times & count
        times = [0] + [inf] * (n-1)
        count = [1] + [inf] * (n-1)
        
        # 3. maintain min-heap (time, node)
        heap = [(0, 0)]

        # 4. loop and explore neighbors
        while heap:
            curt, curn = heappop(heap)

            for nextn, t in adj[curn]:
                nextt = curt + t
                # case: faster || equal || longer
                if nextt == times[nextn]:
                    count[nextn] = (count[nextn] + count[curn]) % mod
                elif nextt < times[nextn]:
                    times[nextn] = nextt
                    count[nextn] = count[curn]
                    heappush(heap, (nextt, nextn))

        return count[-1]