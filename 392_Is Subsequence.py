class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        pt, plen = 0, len(t)
        for curs in s:
            while pt < plen and t[pt] != curs: pt += 1
            if pt == plen: return False
            pt += 1
        return True