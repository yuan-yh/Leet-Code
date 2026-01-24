# Method 1: not choose or choose from [start : len)
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        def bt(start, end):
            res.append(list(curPath))

            for i in range(start, end):
                curPath.append(nums[i])
                bt(i + 1, end)
                curPath.pop()
        
        curPath, res = [], []
        bt(0, len(nums))
        return res

# # Method 2: choose or not choose
# class Solution:
#     def subsets(self, nums: List[int]) -> List[List[int]]:
#         # choose or not choose at nums[i]
#         def bt(start):
#             res.append(list(curPath))

#             for i in range(start, len(nums)):
#                 curPath.append(nums[i])
#                 bt(i+1)
#                 curPath.pop()
        
#         res, curPath = [], []
#         bt(0)
#         return res