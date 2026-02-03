class Solution:
    def longestPalindrome(self, s: str) -> str:
        # 2-ptr expanding from the center
        resL = resR = 0
        length = len(s)

        for i, c in enumerate(s):
            # case 1: odd palindrome
            l = r = i
            while l >= 0 and r < length and s[l] == s[r]:
                l -= 1
                r += 1
            if r-l-1 > resR-resL: resL, resR = l+1, r-1
            # case 2: even palindrome
            l, r = i, i + 1
            while l >= 0 and r < length and s[l] == s[r]:
                l -= 1
                r += 1
            if r-l-1 > resR-resL: resL, resR = l+1, r-1
        
        return s[resL : resR + 1]