class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        # 1. sort to prevent duplicates
        nums.sort()
        # 2. 2Sum
        res = []

        for a in range(len(nums) - 3):
            if a > 0 and nums[a] == nums[a-1]: continue         # trim duplicates
            if nums[a] + nums[-1] + nums[-2] + nums[-3] < target: continue
            if nums[a] + nums[a+1] + nums[a+2] + nums[a+3] > target: break
            
            for b in range(a+1, len(nums) - 2):
                if b > a+1 and nums[b] == nums[b-1]: continue   # trim duplicates
                if nums[a] + nums[b] + nums[-1] + nums[-2] < target: continue
                if nums[a] + nums[b] + nums[b+1] + nums[b+2] > target: break

                l, r = b + 1, len(nums) - 1
                while l < r:
                    if nums[a] + nums[b] + nums[l] + nums[r] == target:
                        res.append([nums[a], nums[b], nums[l], nums[r]])
                        l += 1
                        while l < r and nums[l] == nums[l-1]: l += 1
                        r -= 1
                        while l < r and nums[r] == nums[r+1]: r -= 1
                    elif nums[a] + nums[b] + nums[l] + nums[r] < target:
                        l += 1
                        while l < r and nums[l] == nums[l-1]: l += 1
                    else:
                        r -= 1
                        while l < r and nums[r] == nums[r+1]: r -= 1
        
        return res