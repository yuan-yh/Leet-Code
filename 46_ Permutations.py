class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        def dfs():
            # end case
            if len(curPath) == length:
                res.append(list(curPath))
                return
            
            # process
            for i, n in enumerate(visit):
                if not n:
                    curPath.append(nums[i])
                    visit[i] = True
                    dfs()
                    visit[i] = False
                    curPath.pop()

        length = len(nums)
        visit = [False] * length
        curPath, res = [], []
        dfs()
        return res