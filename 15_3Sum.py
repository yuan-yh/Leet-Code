class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        # 1. sort in ASC order
        nums.sort()
        # 2. for loop - 2Sum
        res = []
        for i in range(len(nums) - 2):
            # 3. avoid duplication & short-cut
            if i > 0 and nums[i] == nums[i-1]: continue
            if nums[i] + nums[-1] + nums[-2] < 0: continue
            if nums[i] + nums[i+1] + nums[i+2] > 0: break

            # 4. 2-ptr for sum-up-to 0
            l, r = i + 1, len(nums) - 1
            while l < r:
                tsum = nums[i] + nums[l] + nums[r]

                if tsum > 0: r -= 1
                elif tsum < 0: l += 1
                else:
                    res.append((nums[i], nums[l], nums[r]))
                    # 5. shift l/r ptr w/n duplicates
                    l, r = l + 1, r - 1
                    while l < r and nums[l] == nums[l-1]: l += 1
                    while l < r and nums[r] == nums[r+1]: r -= 1

        return res