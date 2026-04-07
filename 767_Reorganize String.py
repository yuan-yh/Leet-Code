# Time Complexity: O(n log k).
# O(n + k log k + n log k), 因为 k <= n，通常可以合并为：O(n log k).

class Solution:
    def reorganizeString(self, s: str) -> str:
        # 1. count - O(n)
        count = Counter(s)

        # 2. init heap (default min-heap in python) - O(k log(k))
        heap = []
        for c, cnt in count.items(): heappush(heap, (-cnt, c))
        
        # 3. Greedy - prioritize the most frequent letter - O(n log(k))
        res, prev, pCnt = [], "", 0

        while heap:
            tCnt, tmp = heappop(heap)

            res.append(tmp)
            tCnt += 1

            if pCnt < 0: heappush(heap, (pCnt, prev))
            prev, pCnt = "", 0

            if tCnt < 0: prev, pCnt = tmp, tCnt

        return "" if len(res) < len(s) else ''.join(res)