class Solution:
    def possibleBipartition(self, n: int, dislikes: List[List[int]]) -> bool:
        # 二分图染色法
        groups = [0] * n    # 0 for unvisited, 1 for group1, -1 for group2

        # 4. DFS details
        def dfs(cur: int, group: int) -> bool:
            # A. assign groups
            groups[cur] = group
            # B. explore its diss, check for contradict or future contradict
            for d in diss[cur]:
                if groups[d] == group or (groups[d] == 0 and not dfs(d, -group)):
                    return False
            return True

        # 1. record diss relationship
        diss = defaultdict(list)
        for p1, p2 in dislikes:
            diss[p1 - 1].append(p2 - 1)
            diss[p2 - 1].append(p1 - 1)
        
        # 2. loop ungrouped person
        for i in range(n):
            # 3. DFS
            if groups[i] == 0 and not dfs(i, 1): return False
        
        return True