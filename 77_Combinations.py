class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        curPath, res = [], []

        def dfs(cur, left):
            if left == 0: 
                res.append(list(curPath))
                return
            
            for i in range(cur, n+1):
                # short-cut
                if n-i+1 < left: break
                curPath.append(i)
                dfs(i+1, left-1)
                curPath.pop()

        dfs(1, k)
        return res