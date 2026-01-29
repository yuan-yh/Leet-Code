class Solution:
    def minWindow(self, s: str, t: str) -> str:
        cntS, cntT = Counter(), Counter(t)
        resL, resR, l = -1, len(s), 0

        for r, c in enumerate(s):
            cntS[c] += 1
            while cntS >= cntT:
                if resR-resL > r-l: resL, resR = l, r
                cntS[s[l]] -= 1
                l += 1
        return "" if resL == -1 else s[resL : resR + 1]