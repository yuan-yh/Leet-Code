class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        # Sliding window
        res = []
        pCnt = Counter(p)
        sCnt = Counter()

        for end, c in enumerate(s):
            # 1. update record
            sCnt[c] += 1
            # 2. calculate window start
            start = end - len(p) + 1
            if start < 0: continue
            # 3. check if the cur window matches
            if sCnt == pCnt: res.append(start)
            sCnt[s[start]] -= 1

        return res