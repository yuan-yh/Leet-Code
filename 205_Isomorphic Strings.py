class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        dictT = {}  # key: tc, val: sc
        dictS = {}  # key: sc, val: tc

        for tc, sc in zip(t, s):
            if (tc in dictT and dictT[tc] != sc) or (sc in dictS and dictS[sc] != tc): return False
            dictT[tc] = sc
            dictS[sc] = tc

        return True