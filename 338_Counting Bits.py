class Solution:
    def countBits(self, n: int) -> List[int]:
        res = [0]
        for i in range(1, n+1):
            # case: even = cnt(even >> 1)
            # case: odd = prev_even_cnt + 1
            if i % 2 == 0: res.append(res[i >> 1])
            else: res.append(res[-1] + 1)
        return res