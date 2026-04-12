class Solution:
    def totalFruit(self, fruits: List[int]) -> int:
        if len(fruits) <= 2: return len(fruits)
        # max length of subarray with exactly 2 components
        count = {}
        res = l = 0
        for i, f in enumerate(fruits):
            # 1. update count
            count[f] = count[f] + 1 if f in count else 1
            # 2. validate window
            while len(count) > 2:
                count[fruits[l]] -= 1
                if count[fruits[l]] == 0: del count[fruits[l]]
                l += 1
            # 3. update res
            res = max(res, i - l + 1)
        return res