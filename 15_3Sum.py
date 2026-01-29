class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        # 1. sort
        nums.sort()

        # 2. loop i -> while find j & k
        res = []

        for i in range(len(nums) - 2):
            # avoid duplicates
            if i > 0 and nums[i] == nums[i-1]: continue
            # short-cut
            if nums[i] + nums[-2] + nums[-1] < 0: continue
            if nums[i] + nums[i+1] + nums[i+2] > 0: break

            l, r = i + 1, len(nums) - 1
            while l < r:
                if nums[i] + nums[l] + nums[r] > 0: r -= 1
                elif nums[i] + nums[l] + nums[r] < 0: l += 1
                else:
                    res.append([nums[i], nums[l], nums[r]])
                    l += 1
                    r -= 1
                    # shift to a different j/k values
                    while l < r and nums[l] == nums[l-1]: l += 1
                    while l < r and nums[r] == nums[r+1]: r -= 1
        return res