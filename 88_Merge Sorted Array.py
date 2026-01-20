class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        # Key Insight: fill backwards, so no overlapping issue
        m, n, p = m-1, n-1, m+n-1

        while p >= 0:
            # case 1: pick from nums2
            if m < 0 or (n >= 0 and nums2[n] > nums1[m]):
                nums1[p] = nums2[n]
                n -= 1
            # case 2: pick from nums1
            else:
                nums1[p] = nums1[m]
                m -= 1
            
            p -= 1
            # short-cut
            if n < 0: break