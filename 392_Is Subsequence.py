class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        # Track the next char of s in t while maintain the relative order
        # short-cut
        if len(s) == 0: return True
        if len(t) < len(s): return False

        pt, lent = 0, len(t)
        for curs in s:
            while pt < lent and t[pt] != curs: pt += 1
            # Now either out of t range or t[pt] == curs
            if pt == lent: return False
            pt += 1
        
        return True