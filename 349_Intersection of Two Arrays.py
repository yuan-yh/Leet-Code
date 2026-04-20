class Solution:
    # Method 1
    def intersection(self, n1: List[int], n2: List[int]) -> List[int]:
        n1 = set(n1)
        res = []
        for n in set(n2):
            if n in n1:
                res.append(n)
                n1.remove(n)

        return res
    
    # # Method 2
    # def intersection(self, n1: List[int], n2: List[int]) -> List[int]:
    #     # hashset then compare
    #     n1, n2 = set(n1), set(n2)
    #     return list(n1 & n2)