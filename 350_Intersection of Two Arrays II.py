class Solution:
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        # 1. count nums1 frequency
        cnt1 = Counter(nums1)
        # 2. loop nums2 - if intersection & cnt > 0, decrement by 1
        res = []
        for n in nums2:
            if n in cnt1 and cnt1[n] > 0:
                res.append(n)
                cnt1[n] -= 1
        return res