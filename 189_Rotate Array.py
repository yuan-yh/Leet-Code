class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        length = len(nums)
        k = k % length
        if k == 0: return

        def reverse(start, end):
            while start < end:
                nums[start], nums[end] = nums[end], nums[start]
                start, end = start + 1, end - 1
        
        # 1. reverse the entire array
        reverse(0, length - 1)
        # 2. mirror reflection for the first k elements (nums[:k]) and the rest (nums[k:])
        reverse(0, k - 1)
        reverse(k, length - 1)