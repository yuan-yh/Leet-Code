class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        lh, ln = len(haystack), len(needle)
        for i in range(lh - ln + 1): 
            if haystack[i : i + ln] == needle: return i
        return -1