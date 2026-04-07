class Solution:
    # # 1. Topological Sort
    # def canFinish(self, numCourses: int, preq: List[List[int]]) -> bool:
    #     cnext = [[] for _ in range(numCourses)]
    #     inDeg = [0] * numCourses
        
    #     # 1. init
    #     for a, b in preq:
    #         cnext[b].append(a)
    #         inDeg[a] += 1
        
    #     # 2. loop to process those w/n in-degrees
    #     q = deque()
    #     for i, d in enumerate(inDeg):
    #         if d == 0: q.append(i)
        
    #     cnt = 0
    #     while q:
    #         tmp = q.pop()
    #         cnt += 1

    #         for cn in cnext[tmp]:
    #             inDeg[cn] -= 1
    #             if inDeg[cn] == 0: q.append(cn)
    #     return cnt == numCourses

    # 2. DFS
    def canFinish(self, numCourses: int, preq: List[List[int]]) -> bool:
        # 1. init w/ prep
        cprev = [[] for _ in range(numCourses)]
        for a, b in preq: cprev[a].append(b)

        # 2. init the valid status (0-not check, 1-checking, 2-valid)
        valid = [0] * numCourses

        # 3. dfs for each course, check if each can be completed
        def bt(course: int) -> bool:
            # end case
            if valid[course] == 2: return True
            if valid[course] == 1: return False
            # process
            valid[course] = 1

            for cp in cprev[course]:
                if not bt(cp): return False
            
            valid[course] = 2
            return True
        
        for c in range(numCourses):
            if not bt(c): return False
        return True