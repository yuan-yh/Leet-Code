# # Method 1: BFS - keep processing courses w/n preps
# class Solution:
#     def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
#         indegree = [0] * numCourses
#         cnext = [[] for _ in range(numCourses)]

#         for n, p in prerequisites:
#             cnext[p].append(n)
#             indegree[n] += 1
        
#         q = deque()
#         for c in range(numCourses):
#             if indegree[c] == 0:
#                 q.append(c)
        
#         cnt = 0
#         while q:
#             curC = q.popleft()
#             cnt += 1
#             for n in cnext[curC]:
#                 indegree[n] -= 1
#                 if indegree[n] == 0:
#                     q.append(n)
#         return cnt == numCourses

        
# Method 2: DFS - explore preps of the cur course to check for cycles
class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        def hasCycle(course) -> bool:
            if visit[course] == 1:
                return True
            if visit[course] == 2:
                return False
            
            visit[course] = 1
            for p in cprep[course]:
                if hasCycle(p):
                    return True
            visit[course] = 2
            return False

        visit = [0] * numCourses
        cprep = [[] for _ in range(numCourses)]

        for n, p in prerequisites:
            cprep[n].append(p)
        
        for c in range(numCourses):
            if hasCycle(c):
                return False
        return True        