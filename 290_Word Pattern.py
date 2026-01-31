class Solution:
    def wordPattern(self, pattern: str, s: str) -> bool:
        words = s.split(' ')

        dictW = {}  # key: word, val: pc
        dictP = {}  # key: pc, val: word

        # short-cut
        if len(pattern) != len(words): return False

        for pc, word in zip(pattern, words):
            if (word in dictW and dictW[word] != pc) or (pc in dictP and dictP[pc] != word): return False
            dictW[word] = pc
            dictP[pc] = word
        
        return True