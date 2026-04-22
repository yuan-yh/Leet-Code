class Solution:
    def findMedianSortedArrays(self, n1: List[int], n2: List[int]) -> float:
        # Find i and j in n1 and n2 such that n1[i] < n2[j+1]
        # 1. assign n1 the longer array
        if len(n2) > len(n1): n1, n2 = n2, n1

        # 2. calculate the left-half size (+1 if odd total)
        l1, l2 = len(n1), len(n2)
        lhalf = (l1 + l2 + 1) // 2

        # 3. Binary Search for i in range: [ all_n2_is_left, all_left_in_n1]
        il, ir = lhalf-l2-1, lhalf-1
        while il < ir:
            m = (il + ir + 1) >> 1
            j = lhalf - m - 2

            lmed1 = n1[m] if m >= 0 else -inf
            rmed2 = n2[j+1] if j+1 < l2 else inf
            if lmed1 < rmed2: il = m
            else: ir = m - 1

        # 4. return median based on even/odd total
        i, j = il, lhalf - il - 2
        lmed1 = n1[i] if i >= 0 else -inf
        rmed1 = n1[i+1] if i+1 < l1 else inf
        lmed2 = n2[j] if j >= 0 else -inf
        rmed2 = n2[j+1] if j+1 < l2 else inf

        lmed, rmed = max(lmed1, lmed2), min(rmed1, rmed2)
        return lmed if (l1 + l2) % 2 == 1 else (lmed + rmed) / 2