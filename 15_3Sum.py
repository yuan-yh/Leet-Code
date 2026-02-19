class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        # Key Insight: not idx in res -> sort
        res = []

        # 1. sort
        nums.sort()
        # 2. outer loop: i in [0, len-2)
        for i in range(len(nums) - 2):
            # 3. short-cut: avoid duplicate; sum(i, -1, -2) < 0; sum([i:i+2]) > 0
            if i > 0 and nums[i] == nums[i-1]: continue
            if nums[i] + nums[-2] + nums[-1] < 0: continue
            if nums[i] + nums[i+1] + nums[i+2] > 0: break

            # 4. inner loop: 2-ptr to i+1 and len-1
            j, k = i + 1, len(nums) - 1
            while j < k:
                tmp = nums[i] + nums[j] + nums[k]
                if tmp < 0: j += 1
                elif tmp > 0: k -= 1
                else: 
                    res.append([nums[i], nums[j], nums[k]])
                    j += 1
                    k -= 1
                    # 5. shift ptr to avoid duplicates
                    while j < k and nums[j] == nums[j-1]: j += 1
                    while j < k and nums[k] == nums[k+1]: k -= 1

        return res