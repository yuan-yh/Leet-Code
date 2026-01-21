class Solution:
    def candy(self, ratings: List[int]) -> int:
        # Similar to LC 134: 折线图 -> focus on the 严格递增段 (viewing leftwards & rightwards)
        # 1. Baseline: each with at least one candy
        length = len(ratings)
        res = [1] * length
        # 2. More candies w/ higher ratings = 严格递增段, peak = prev + 1
        # 2.1 check the string-increasing from left to right
        for i in range(1, length):
            if ratings[i] > ratings[i-1]: 
                res[i] = res[i-1] + 1
        # 2.2 check the string-increasing from right to left
        for i in range(length - 2, -1, -1):
            if ratings[i] > ratings[i+1] and res[i] <= res[i+1]:
                res[i] = res[i+1] + 1
        return sum(res)