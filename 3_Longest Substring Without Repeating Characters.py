class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        # 2-ptr to maintain the window & hashmap to track letter idx
        res = start = 0
        record = {} # key: letter, val: idx

        for right, c in enumerate(s): 
            # 1. check if the last cur_letter in this window
            if c in record and record[c] >= start:
                # 2. if yes, shift start
                start = record[c] + 1
            # 3. update letter idx
            record[c] = right
            # 4. update res
            res = max(res, right - start + 1)
        return res