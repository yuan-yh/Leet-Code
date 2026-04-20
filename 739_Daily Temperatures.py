class Solution:
    # Method 1: left-to-right, both O(n)
    def dailyTemperatures(self, temp: List[int]) -> List[int]:
        res = [0] * len(temp)
        q = []
        for i in range(len(temp)):
            # case: empty || temp[q[-1]] < cur || temp[q[-1]] >= cur
            while q and temp[q[-1]] < temp[i]:
                res[q[-1]] = i - q[-1]
                q.pop()
            q.append(i)
        return res
    
    # # Method 2: right-to-left
    # def dailyTemperatures(self, temp: List[int]) -> List[int]:
    #     res = []
    #     q = deque()     # (idx)
    #     for i in range(len(temp)-1, -1, -1):
    #         # case: empty q: append
    #         # case: cur_temp >= temp[q[-1]]: keep pop
    #         #   if empty: append
    #         #   if not: calculate idx then append
    #         # case: cur_temp < temp[q[-1]]: calculate idx then append
    #         while q and temp[q[-1]] <= temp[i]: q.pop()
    #         res.append(0 if not q else q[-1] - i)
    #         q.append(i)
        
    #     # reverse res
    #     l, r = 0, len(res) - 1
    #     while l < r:
    #         res[l], res[r] = res[r], res[l]
    #         l, r = l + 1, r - 1
    #     return res