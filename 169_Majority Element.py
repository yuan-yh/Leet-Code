class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        # 摩尔投票 (严格众数): 同一值 -> cnt加 1，否则值减 1
        cnt, val = 0, nums[0]
        for i in nums:
            if cnt == 0 or i == val:
                val = i
                cnt += 1
            else: cnt -= 1
        return val