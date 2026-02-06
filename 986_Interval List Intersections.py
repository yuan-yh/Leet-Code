class Solution:
    def intervalIntersection(self, n1: List[List[int]], n2: List[List[int]]) -> List[List[int]]:
        # Two-pointer: when intersection, append([max(start1, start2), min(end1, end2)])
        p1, p2, l1, l2 = 0, 0, len(n1), len(n2)
        res = []

        while p1 < l1 and p2 < l2:            
            # case: intersection: max(start1, start2) <= min(end1, end2)
            left, right = max(n1[p1][0], n2[p2][0]), min(n1[p1][1], n2[p2][1])

            if left <= right: res.append([left, right])
            # update: shift the ptr w/ smaller end
            if n1[p1][1] < n2[p2][1]: p1 += 1
            else: p2 += 1
        return res