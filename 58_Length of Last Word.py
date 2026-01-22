class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        slist = s.strip().split(" ")
        return len(slist[-1])