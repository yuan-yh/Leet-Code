class Solution:
    def splitArray(self, nums: List[int], k: int) -> int:
        # 1. calculate ideal sub_sum = total / k
        # 2. slide window w/ sum closest to the ideal sub_sum