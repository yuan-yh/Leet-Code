MAPPING = "", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"

class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        def bt(idx, end):
            # end case
            if idx == end:
                res.append(''.join(curPath))
                return
            # process
            for c in MAPPING[int(digits[idx])]:
                curPath.append(c)
                bt(idx + 1, end)
                curPath.pop()
                
        curPath, res = [], []
        bt(0, len(digits))
        return res