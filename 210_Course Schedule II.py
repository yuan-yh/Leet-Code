class Solution:
    # # Method 1: topological sort
    # def findOrder(self, numCourses: int, preq: List[List[int]]) -> List[int]:
    #     # 1. build adj-list & record in-degree
    #     adj = [[] for _ in range(numCourses)]
    #     indegree = [0] * numCourses

    #     for a, b in preq:
    #         adj[b].append(a)
    #         indegree[a] += 1
        
    #     # 2. start from no-in-degree
    #     q = deque()
    #     for i in range(numCourses):
    #         if indegree[i] == 0: q.append(i)
        
    #     path = []
    #     while q:
    #         tmp = q.popleft()
    #         path.append(tmp)
    #         for cnext in adj[tmp]:
    #             indegree[cnext] -= 1
    #             if indegree[cnext] == 0: q.append(cnext)
        
    #     return path if len(path) == numCourses else []

    # Method 2: DFS
    def findOrder(self, numCourses: int, preq: List[List[int]]) -> List[int]:
        def dfs(course: int) -> bool:
            # 3. check for cycle or verified results
            if visit[course] == 1: return False
            if visit[course] == 2: return True
            # 4. check for prev then update paths
            visit[course] = 1
            for p in prep[course]:
                if not dfs(p): return False
            visit[course] = 2
            path.append(course)
            return True

        # 1. build prep list
        prep = [[] for _ in range(numCourses)]
        visit = [0] * numCourses

        for a, b in preq: prep[a].append(b)

        # 2. loop each course to check for cycle
        path = []
        for i in range(numCourses):
            if not dfs(i): return []
        return path