class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        # look for window of words in s
        res = []
        # 1. count words
        cntw = Counter(words)
        lw, lws = len(words[0]), len(words)

        # 2. divide into lw groups, each group start w/ i and share the same sliding window records
        # For example: 0, lw, 2lw,,,; 1, 1+lw, 1+2lw,,,
        for i in range(lw):
            l = i
            cnts = defaultdict(int)
            valids = 0

            # 3. loop s by word chunks
            for r in range(i, len(s)-lw+1, lw):
                curw = s[r : r + lw]
                # 3.1 cur word not in words: re-init and shift the left ptr
                if curw not in cntw:
                    l = r + lw
                    cnts.clear()
                    valids = 0
                    continue
                # 3.2 update cur word count
                cnts[curw] += 1
                valids += 1
                # 3.3 cur word count exceeds counts in words
                while cnts[curw] > cntw[curw]:
                    cnts[s[l : l+lw]] -= 1
                    l += lw
                    valids -= 1
                # 3.4 valid count match -> record res
                if valids == lws: res.append(l)
        
        return res