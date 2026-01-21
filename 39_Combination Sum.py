class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        # 完全背包: 每个物品可以用无限次
        # At each c[i], you may not choose or choose from [i:]
        res, curPath = [], []

        def bt(start, curSum):
            # end case
            if curSum == target:
                res.append(list(curPath))
                return
            # process
            for i in range(start, len(candidates)):
                # cut branch
                if curSum + candidates[i] > target: break

                curPath.append(candidates[i])
                bt(i, curSum + candidates[i])
                curPath.pop()
        
        candidates.sort()
        bt(0, 0)
        return res