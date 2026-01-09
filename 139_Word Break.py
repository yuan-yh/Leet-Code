class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        # For each substring s[:i] inclusively, check if it can be filled with wDict
        wDict = set(wordDict)
        n = len(s)
        dp = [True] + [False] * n

        for i in range(n):
            for w in wDict:
                # check s[i+1 - len(w) : i+1]
                if i+1 - len(w) < 0: continue
                if s[i+1 - len(w) : i+1] == w: dp[i+1] = dp[i+1] or dp[i+1 - len(w)]    # avoid overlapping w/ prev record
        return dp[n]