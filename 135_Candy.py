class Solution:
    def candy(self, ratings: List[int]) -> int:
        # Basedline: 1 candy; higher grade = more candy than neighbors
        length = len(ratings)
        left, right = [1] * length, [1] * length
        
        # 從左向右看，登高一步+1
        for i in range(1, length):
            if ratings[i] > ratings[i-1]:
                left[i] = left[i-1] + 1
        
        # 從右向左看，登高一步+1
        for i in range(length - 2, -1, -1):
            if ratings[i] > ratings[i+1]:
                right[i] = right[i+1] + 1

        # Count total
        res = 0
        for i in range(length):
            res += max(left[i], right[i])
        return res