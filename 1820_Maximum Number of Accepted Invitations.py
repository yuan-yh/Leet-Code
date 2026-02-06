class Solution:
    def maximumInvitations(self, grid: List[List[int]]) -> int:
        # 匈牙利算法: 让当前占用右节点的人去找别人
        boys, girls = len(grid), len(grid[0])
        gmatch = [-1] * girls

        # 2. DFS
        def dfs(cur: int, visited) -> bool:
            # 3. loop in cur's available match
            for girl, match in enumerate(grid[cur]):
                # 4. check for unvisited match
                if match == 1 and girl not in visited:
                    visited.add(girl)
                    # 5. success case: girl not match yet || prev matching target can switch to other girls
                    if gmatch[girl] == -1 or dfs(gmatch[girl], visited):
                        gmatch[girl] = cur
                        return True
            return False

        res = 0
        # 1. loop boys - increment res by 1 if there is a match through DFS
        for b in range(boys):
            if dfs(b, set()): res += 1
        return res