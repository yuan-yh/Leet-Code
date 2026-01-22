class Solution:
    def romanToInt(self, s: str) -> int:
        record = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        q = deque()
        for c in s:
            q.append(record[c])
        
        res = prev = q.pop()
        while q:
            cur = q.pop()
            if cur < prev: res -= cur
            else: res += cur

            prev = cur
        
        return res