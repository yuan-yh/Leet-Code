class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        res = ""
        for w1, w2 in zip(word1, word2):
            res += w1 + w2
        
        l1, l2 = len(word1), len(word2)
        if l1 > l2: res += word1[l2:]
        else: res += word2[l1:]
        return res