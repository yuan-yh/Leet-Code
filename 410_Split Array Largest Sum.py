class Solution:
    def splitArray(self, nums: List[int], k: int) -> int:
        # min_sub_sum in range [max_n : total_sum] -> binary search
        # 1. init boundary
        l = r = 0
        for n in nums:
            l = max(l, n)
            r += n
        
        # 3. simulation
        def check(target: int) -> bool:
            prev, cnt = 0, 1
            for n in nums:
                if prev + n > target:
                    cnt += 1
                    prev = n
                else: prev += n
                if cnt > k: return False
            return True
        
        # 2. binary search in [l:r]
        while l < r:
            m = (l + r) >> 1
            if check(m): r = m
            else: l = m + 1
        return l