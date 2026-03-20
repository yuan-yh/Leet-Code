class Solution:
    # # Method 1: topological sort
    # def canFinish(self, numCourses: int, preq: List[List[int]]) -> bool:
    #     # 1. build adj list & record in-degree
    #     adj = [[] for _ in range(numCourses)]
    #     indegree = [0] * numCourses

    #     for a, b in preq:
    #         adj[b].append(a)
    #         indegree[a] += 1

    #     # 2. start from those w/n in-degree
    #     q = deque()
    #     cnt = 0
    #     for c, ind in enumerate(indegree):
    #         if ind == 0: q.append(c)

    #     while q:
    #         curC = q.popleft()
    #         cnt += 1
    #         for nextC in adj[curC]:
    #             indegree[nextC] -= 1
    #             if indegree[nextC] == 0: q.append(nextC)
        
    #     return cnt == numCourses

    # Method 2: DFS
    def canFinish(self, numCourses: int, preq: List[List[int]]) -> bool:
        def dfs(course: int) -> bool:
            # 3. Cycle Check: if the curCourse in the curPath
            if visit[course] == 1: return False
            if visit[course] == 2: return True
            visit[course] = 1

            # 4. Update Succes course record to trim branch
            for p in prep[course]:
                if not dfs(p): return False
            visit[course] = 2
            return True

        # 1. build prep_list for each course
        prep = [[] for _ in range(numCourses)]
        visit = [0] * numCourses    # 0: uncheck, 1: in progress, 2: verified

        for a, b in preq: prep[a].append(b)

        # 2. check each course for cyle by DFS its preq
        for c in range(numCourses): 
            if not dfs(c): return False
        return True