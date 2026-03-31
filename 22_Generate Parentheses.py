class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        def bt(openLeft: int, closeLeft: int):
            # end case
            if closeLeft == 0:
                res.append(''.join(curPath))
                return
            # choose to ')' or not
            if closeLeft > openLeft:
                curPath.append(')')
                bt(openLeft, closeLeft-1)
                curPath.pop()
            if openLeft > 0:
                curPath.append('(')
                bt(openLeft-1, closeLeft)
                curPath.pop()

        curPath, res = [], []
        bt(n, n)
        return res