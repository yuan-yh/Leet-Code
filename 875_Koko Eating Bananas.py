class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        # res in [1, max(piles[i])]
        # 1. short-cut: if h == len(piles)
        maxp = 0
        for p in piles: maxp = max(maxp, p)

        # 2. Binary search in [1, maxp]
        def mock(speed) -> int:
            time = 0
            for p in piles:
                time += p // speed
                if p%speed != 0: time += 1
            return time

        l, r = 1, maxp
        while l < r:
            m = (l + r) >> 1
            if mock(m) <= h: r = m
            else: l = m+1
        return l