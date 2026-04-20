class Solution:
    # # Method 1: choose or not choose
    # def subsets(self, nums: List[int]) -> List[List[int]]:
    #     def bt(idx: int):
    #         if idx == len(nums):
    #             res.append(list(curPath))
    #             return
    #         bt(idx + 1)
    #         curPath.append(nums[idx])
    #         bt(idx + 1)
    #         curPath.pop()
    #     res, curPath = [], []
    #     bt(0)
    #     return res
    
    # Method 2: choose from a given range
    def subsets(self, nums: List[int]) -> List[List[int]]:
        def bt(idx: int):
            res.append(list(curPath))
            for i in range(idx, len(nums)):
                curPath.append(nums[i])
                bt(i + 1)
                curPath.pop()
        res, curPath = [], []
        bt(0)
        return res