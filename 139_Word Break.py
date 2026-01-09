class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        # For s[:i] inclusively, check if can be filled by wDict
        wDict = set(wordDict)
        n = len(s)
        dp = [True] + [False] * n
        
        for i in range(n):
            for w in wDict:
                # match s[i+1 - len(w) : i+1]
                if i+1 - len(w) < 0: continue
                if s[i+1 - len(w) : i+1] == w: dp[i+1] = dp[i+1] or dp[i+1-len(w)]

        return dp[n]