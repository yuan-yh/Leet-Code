```python
class Solution:
    def minboard(self, roof: List[List[int]]) -> int:
        # Key: max match of row & col
        # 1. init col_match w/ -1
        row, col = len(roof), len(roof[0])
        cmatch = [-1] *col

        # 3. DFS(row, set()) -> bool
        def dfs(cur, visited) -> bool:
            for c, hole in enumerate(roof[cur]):
                # A. check for hole and unvisited -> update
                if hole == 0 and c not in visited:
                    visited.add(c)
                    # B. check for not matched || can switch prev_match to other col
                    if cmatch[c] == -1 or dfs(cmatch[c], visited):
                        cmatch[c] = cur
                        return True
            return False

        # 2. loop row -> res += 1 if match via DFS
        res = 0
        for r in range(row):
            if dfs(r, set()): res += 1
        return res
```

I practiced again the min boards to fix the roof question, is the code right?