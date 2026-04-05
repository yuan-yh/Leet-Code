class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        def bt(openP, closeP):
            # end case
            if openP == n and closeP == n:
                res.append(''.join(curPath))
                return
            # process: choose ) or not
            if openP > closeP: 
                curPath.append(')')
                bt(openP, closeP + 1)
                curPath.pop()
            if openP < n:
                curPath.append('(')
                bt(openP + 1, closeP)
                curPath.pop()

        res, curPath = [], []
        bt(0, 0)
        return res