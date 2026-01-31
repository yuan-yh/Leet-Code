class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        record = set()

        for r in range(len(nums)):
            # 0. check the window
            if nums[r] in record: return True
            # 1. add the cur digit
            record.add(nums[r])
            # 2. pre-maintain the left boundary if r >= k
            if r >= k: record.remove(nums[r-k])

        return False