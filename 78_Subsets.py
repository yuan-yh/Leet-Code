class Solution:
    # # Method 1: choose or not choose
    # def subsets(self, nums: List[int]) -> List[List[int]]:
    #     def dfs(idx, end):
    #         # end case
    #         if idx == end:
    #             res.append(list(curPath))
    #             return
    #         # process: choose or not choose
    #         dfs(idx + 1, end)
    #         curPath.append(nums[idx])
    #         dfs(idx + 1, end)
    #         curPath.pop()
        
    #     res, curPath = [], []
    #     dfs(0, len(nums))
    #     return res
    
    # Method 2: not choose or choose from range
    def subsets(self, nums: List[int]) -> List[List[int]]:
        def dfs(start, end):
            res.append(list(curPath))

            for i in range(start, end):
                curPath.append(nums[i])
                dfs(i + 1, end)
                curPath.pop()

        
        res, curPath = [], []
        dfs(0, len(nums))
        return res