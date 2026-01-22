class Solution:
    def convert(self, s: str, numRows: int) -> str:
        # edge case
        if numRows == 1: return s

        # change direction: if curRow == 0 -> down (+1); if curRow == numRows - 1 -> up (-1)
        res = [""] * numRows

        curRow, d = 0, -1
        for c in s:
            res[curRow] += c
            if curRow == 0 or curRow == numRows - 1: d = -d
            curRow += d
        return ''.join(res)