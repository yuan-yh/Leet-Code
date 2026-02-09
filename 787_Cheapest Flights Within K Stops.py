class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        # Key Insight: find the cheapest path w/in k intermediate stops -> Dijkstra
        # 1. build adj list
        adj = [[] for _ in range(n)]
        for s, d, p in flights:
            adj[s].append((d, p))
        # 2. init prices[] & set src 0
        prices = [inf] * n
        prices[src] = 0
        # 3. build min-heap (stop, price, node)
        heap = [(0, 0, src)]
        # 4. loop to explore next stops (skip if stop > k or price)
        while heap:
            curstop, curp, curn = heappop(heap)
            if curstop == k+1: continue

            for nextn, p in adj[curn]:
                nextp = curp + p
                if nextp < prices[nextn]:
                    prices[nextn] = nextp
                    heappush(heap, (curstop+1, nextp, nextn))

        return -1 if prices[dst] == inf else prices[dst]