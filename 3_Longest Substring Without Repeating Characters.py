class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        # 1. init records for characters w/ corresponding last visited index
        res = left = 0
        record = {}
        # 2. loop
        for i, c in enumerate(s):
            # 3. shrink the left-window when repeating
            if c in record and record[c] >= left: left = record[c] + 1
            record[c] = i
            res = max(res, i - left + 1)
        return res