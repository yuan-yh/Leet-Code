class Solution:
    def findMedianSortedArrays(self, n1: List[int], n2: List[int]) -> float:
        # 1. assign n1 the longer array
        if len(n1) < len(n2): n1, n2 = n2, n1

        # 2. calculate the left-half size (longer if odd total)
        len1, len2 = len(n1), len(n2)
        total = len1 + len2
        left_half = (total + 1) >> 1

        # 3. mark i, j the last idx of left-half[]
        # 4. range of i in: [ all_n2_is_left, all_left_in_n1]
        iL, iR = left_half - len2 - 1, left_half - 1

        while iL < iR:  # [iL, iR]
            iM = (iL + iR + 1) >> 1
            j = left_half - iM - 2

            lastN1L =  n1[iM] if iM >= 0 else -inf
            firstN2R = n2[j+1] if j+1 < len2 else inf

            # 5. ideal: max(n1[i], n2[j]) < min(n1[i+1], n2[j+1])
            if lastN1L > firstN2R: iR = iM - 1
            else: iL = iM
        
        # 6. return based on even / odd total
        i = iL
        j = left_half - i - 2

        lastN1L =  n1[i] if i >= 0 else -inf
        lastN2L =  n2[j] if j >= 0 else -inf
        firstN1R = n1[i+1] if i+1 < len1 else inf
        firstN2R = n2[j+1] if j+1 < len2 else inf
        left = max(lastN1L, lastN2L)
        right = min(firstN1R, firstN2R)
        
        return left if total % 2 == 1 else (left + right) / 2