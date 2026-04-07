class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        # 1. sort
        nums.sort()

        # 2. 2Sum
        res = inf

        for i in range(len(nums) - 2):
            # Trim branch
            # case: min_sum > target => more diff later => terminate
            min_sum = nums[i] + nums[i+1] + nums[i+2]
            if min_sum > target:
                if abs(target - min_sum) < abs(target - res): res = min_sum
                break
            # case: max_sum < target => skip & increase i ASAP
            max_sum = nums[i] + nums[-1] + nums[-2]
            if max_sum < target:
                if abs(target - max_sum) < abs(target - res): res = max_sum
                continue

            l, r = i + 1, len(nums) - 1
            while l < r:
                tsum = nums[i] + nums[l] + nums[r]
                if abs(target - tsum) < abs(target - res): res = tsum

                if tsum > target: r -= 1
                elif tsum < target: l += 1
                else: break
        return res