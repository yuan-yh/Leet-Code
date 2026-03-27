class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        # 完全背包: 每个物品可以用无限次
        # Build a N-nary tree: either not choose or choose from [start:]
        def bt(idx, curSum):
            # end case
            if curSum == target:
                res.append(list(curPath))
                return
            # process
            for i in range(idx, len(candidates)):
                # short-cut: terminate when > target
                if candidates[i] + curSum > target: break
                # short-cut: skip to avoid duplicates
                if i > idx and candidates[i] == candidates[idx]: continue
                curPath.append(candidates[i])
                bt(i, curSum + candidates[i])
                curPath.pop()
        
        # 1. sort
        candidates.sort()
        # 2. bt
        curPath, res = [], []
        bt(0, 0)
        return res