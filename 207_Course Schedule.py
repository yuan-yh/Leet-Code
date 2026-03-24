class Solution:
    # # Method 1: topological sort
    # def canFinish(self, numCourses: int, preq: List[List[int]]) -> bool:
    #     # 1. build adj-list & record in-degree
    #     cnext = [[] for _ in range(numCourses)]
    #     indegree = [0] * numCourses

    #     for a, b in preq:
    #         cnext[b].append(a)
    #         indegree[a] += 1
        
    #     # 2. start from those w/n in-degree
    #     q = deque()
    #     for c, ind in enumerate(indegree):
    #         if ind == 0: q.append(c)
        
    #     cnt = 0
    #     while q:
    #         tmp = q.popleft()
    #         cnt += 1

    #         for c in cnext[tmp]:
    #             indegree[c] -= 1
    #             if indegree[c] == 0: q.append(c)
    #     return cnt == numCourses
        
    # Method 2: DFS
    def canFinish(self, numCourses: int, preq: List[List[int]]) -> bool:
        # for each class, track to preq to see if it can be finished
        cprev = [[] for _ in range(numCourses)]
        visit = [0] * numCourses

        def dfs(course: int) -> bool:
            # 2. check for loop or verified ressults
            if visit[course] == 1: return False
            if visit[course] == 2: return True
        
            # 3. update the status then check for its preq
            visit[course] = 1
            for cp in cprev[course]: 
                if not dfs(cp): return False
            # 4. update to verified
            visit[course] = 2
            return True

        # 1. build prep for each class
        for a, b in preq: cprev[a].append(b)
        
        for c in range(numCourses):
            if not dfs(c): return False

        return True