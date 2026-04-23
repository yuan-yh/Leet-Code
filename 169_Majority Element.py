class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        # 摩尔投票 (严格众数): 同一值 -> cnt加 1，否则值减 1
        major, mcnt = nums[0], 0

        for n in nums:
            if major == n or mcnt == 0:
                major = n
                mcnt += 1
            else:
                mcnt -= 1
        return major