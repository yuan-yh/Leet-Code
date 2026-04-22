class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        # Monotonic Stack
        # 1. track digits in nums1 only
        record = {}
        for i, n in enumerate(nums1): record[n] = i
        # 2. track next-greater in nums2 while focus on those in nums1 only
        res = [-1] * len(nums1)
        q = []
        for n in nums2:
            # case: cur > q[-1]
            while q and n > q[-1]:
                tmp = q.pop()
                res[record[tmp]] = n
            # case: cur < q[-1]
            if n in record: q.append(n)
        return res