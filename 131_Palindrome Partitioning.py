class Solution:
    def partition(self, s: str) -> List[List[str]]:
        @lru_cache(None)
        def isPalindrom(left, right) -> bool:
            if left > right: return False
            while left < right:
                if s[left] != s[right]: return False
                left += 1
                right -= 1
            return True

        def dfs(start: int, idx: int):
            # end case
            if idx == len(s):
                if isPalindrom(start, idx-1):
                    curPath.append(s[start: idx])
                    res.append(list(curPath))
                    curPath.pop()
                return
            
            # split s[start:idx] or not
            if isPalindrom(start, idx-1):
                curPath.append(s[start: idx])
                dfs(idx, idx+1)
                curPath.pop()
            dfs(start, idx+1)

        curPath, res = [], []
        dfs(0, 0)
        return res