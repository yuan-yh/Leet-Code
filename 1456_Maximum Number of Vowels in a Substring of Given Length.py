class Solution:
    def maxVowels(self, s: str, k: int) -> int:
        vowel = {'a', 'e', 'i', 'o', 'u'}
        res = l = 0
        # 1. init window: [0, k)
        for i in range(k):
            if s[i] in vowel: res += 1
        
        cur = res
        # 2. shift window
        for r in range(k, len(s)):
            if s[r] in vowel: cur += 1
            if s[l] in vowel: cur -= 1
            l += 1
            res = max(res, cur)
            # short-cut: find the max case of k valid vowels
            if res == k: break
        
        return res