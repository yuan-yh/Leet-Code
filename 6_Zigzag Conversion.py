class Solution:
    def convert(self, s: str, numRows: int) -> str:
        # Edge case
        if numRows == 1: return s

        # ZigZag = Down -> Up -> Down -> ...
        res = [""] * numRows
        # 1. init w/ the first row & downwards
        r, d = 0, -1

        # 2. loop the given word
        for c in s:
            res[r] += c
            # 3. change direction when touch boundary
            if r == 0 or r == numRows - 1: d = -d
            r += d

        return ''.join(res)