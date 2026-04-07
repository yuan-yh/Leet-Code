class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        def bt(idx: int):
            # end case
            if idx == len(digits):
                res.append(''.join(curPath))
                return
            
            # process
            for c in MAPPINGS[int(digits[idx]) - 2]:
                curPath.append(c)
                bt(idx + 1)
                curPath.pop()

        MAPPINGS = ["abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"]

        res, curPath = [], []
        bt(0)
        return res