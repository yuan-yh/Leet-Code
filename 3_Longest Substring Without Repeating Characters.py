class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        record = {} # key: char, val: the latest visited idx
        res = start = 0

        for i, c in enumerate(s):
            if c in record and record[c] >= start: start = record[c] + 1
            record[c] = i
            
            res = max(i-start+1, res)
        return res