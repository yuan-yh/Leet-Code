class Solution:
    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:
        # 1. assign words in each line
        lines, curLine = [], []
        wcnt = 0
        for word in words:
            # init a new line if exceed maxWidth
            if wcnt + len(curLine) + len(word) > maxWidth:
                lines.append(list(curLine))
                curLine = []
                wcnt = 0
            curLine.append(word)
            wcnt += len(word)
        if len(curLine) > 0: lines.append(list(curLine))
        # 2. insert spaces
        res = []
        for i, line in enumerate(lines):
            tmp = ""
            wcnt = 0
            for w in line: wcnt += len(w)
            slot = len(line) - 1
            scnt = maxWidth - wcnt
            if slot > 0: base, extra = scnt // slot, scnt % slot

            for j, word in enumerate(line):
                tmp += word
                # 3. space processing
                # 1) one-word line
                if slot == 0: tmp += " "*scnt
                # 2) last line: prev vs last word
                elif i == len(lines)-1:
                    if j == len(line) - 1: tmp += " "*scnt
                    else:
                        tmp += " "
                        scnt -= 1
                # 3) other: distribute extras left-to-right, no space for the last word
                elif j < len(line) - 1:
                    tmp += " "*base
                    if extra > 0:
                        tmp += " "
                        extra -= 1
            res.append(tmp)
        return res
        
"""
Requirement:
1. for one-word or last line: left-align, no extra spaces between
2. for others: try distribute spaces evenly, place extras on the lefter slots, no space for the last word
"""