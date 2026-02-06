class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        s1 = set(nums1)
        res = []
        for n in nums2:
            if n in s1:
                s1.remove(n)
                res.append(n)
        
        return res