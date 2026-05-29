class Solution:
    # # BFS
    # def minimumSemesters(self, n: int, relations: List[List[int]]) -> int:
    #     # 1. build in-degree and adj-list(cnext)
    #     indeg = [0] * n
    #     cnext = [[] for _ in range(n)]

    #     for prevc, nextc in relations:
    #         indeg[nextc - 1] += 1
    #         cnext[prevc - 1].append(nextc - 1)
        
    #     # 2. init from 0 in-degree as the 1st semester, cnt course number
    #     q = deque()
    #     complete = semester = 0

    #     for c, d in enumerate(indeg):
    #         if d == 0: q.append(c)
        
    #     # 3. process q
    #     while q:
    #         length = len(q)
    #         semester += 1
    #         for _ in range(length):
    #             curc = q.popleft()
    #             complete += 1
    #             for cn in cnext[curc]:
    #                 indeg[cn] -= 1
    #                 if indeg[cn] == 0: q.append(cn)

    #     return semester if complete == n else -1
    
    # DFS
    def minimumSemesters(self, n: int, relations: List[List[int]]) -> int:
        # 1. build visit-array and adj-list(cprev)
        visit = [0] * n
        cprev = [[] for _ in range(n)]

        for prevc, nextc in relations:
            cprev[nextc - 1].append(prevc - 1)
        
        # 0: un-verify, -1: verifying, >0: verified
        def dfs(curc: int) -> int:
            if visit[curc] < 0: return -1
            if visit[curc] > 0: return visit[curc]

            visit[curc] = -1
            res = 1
            for cp in cprev[curc]:
                tmp = dfs(cp)
                if tmp == -1: return -1
                res = max(res, tmp + 1)
            visit[curc] = res
            return visit[curc]
        
        # 2. loop in courses, terminate when cycle
        for c in range(n):
            if dfs(c) == -1: return -1
        return max(visit)