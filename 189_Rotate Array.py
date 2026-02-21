class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        # 0. 2-line short-cut
        k = k % len(nums)
        nums[:] = nums[-k:] + nums[:-k]

        # # 1. k % len(nums) to minimize rotate steps -> no change if 0
        # k = k % len(nums)
        # if k == 0: return

        # def mirror(left: int, right: int):
        #     while left < right:
        #         nums[left], nums[right] = nums[right], nums[left]
        #         left += 1
        #         right -= 1
        
        # # 2. mirror nums[:]
        # mirror(0, len(nums) - 1)
        
        # # 3. mirror nums[:k) and nums[k:]
        # mirror(0, k-1)
        # mirror(k, len(nums)-1)