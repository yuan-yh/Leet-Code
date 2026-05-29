class Solution:
    # # DFS
    # def minimumSemesters(self, n: int, relations: List[List[int]]) -> int:
    #     # 1. build visit_array & adj_list (cprev)
    #     visit = [0] * n
    #     cprev = [[] for _ in range(n)]
    #     for prevc, nextc in relations:
    #         cprev[nextc - 1].append(prevc - 1)
        
    #     # 0: unverify, -1: verifying, >0: verified
    #     def dfs(curc: int) -> int:
    #         if visit[curc] != 0: return visit[curc]

    #         visit[curc] = res = -1

    #         for cp in cprev[curc]:
    #             tmp = dfs(cp)
    #             if tmp == -1: return -1
    #             res = min(res, - tmp - 1)
    #         visit[curc] = -res
    #         return visit[curc]
    #     # 2. loop each course
    #     for c in range(n):
    #         if dfs(c) == -1: return -1
    #     return max(visit)

    # BFS
    def minimumSemesters(self, n: int, relations: List[List[int]]) -> int:
        # 1. build in-degree & adj_list (cnext)
        indeg = [0] * n
        cnext = [[] for _ in range(n)]

        for prevc, nextc in relations:
            cnext[prevc - 1].append(nextc - 1)
            indeg[nextc - 1] += 1
        
        # 2. push those w/n in-degree into queue
        q = deque()
        for c, ind in enumerate(indeg):
            if ind == 0: q.append(c)
        
        # 3. loop queue & count complete
        complete = semester = 0
        while q:
            length = len(q)
            semester += 1
            for _ in range(length):
                curc = q.popleft()
                complete += 1
                for cn in cnext[curc]:
                    indeg[cn] -= 1
                    if indeg[cn] == 0: q.append(cn)
        return semester if complete == n else -1