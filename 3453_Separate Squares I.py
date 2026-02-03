class Solution:
    def separateSquares(self, squares: List[List[int]]) -> float:
        # Binary search in range [0, max_yi+li]
        left, right = 0, max(y + l for x, y, l in squares)
        total = sum(l * l for x, y, l in squares)

        def check(line) -> bool:
            below = 0
            for x, y, l in squares:
                if y >= line: continue
                below += l * (min(line, y + l) - y)
            return below >= total/2

        while right - left > 1e-5:
            mid = (left + right) / 2
            
            if check(mid): right = mid
            else: left = mid

        return right