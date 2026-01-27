class Solution:
    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:
        # 1. track words assigned in each line
        lines, curRow = [], []
        cnt = 0
        for word in words:
            if cnt != 0 and cnt + len(curRow) + len(word) > maxWidth:
                lines.append(curRow)
                curRow = []
                cnt = 0
            curRow.append(word)
            cnt += len(word)
        if len(curRow) > 0: lines.append(curRow)
        
        # 2. assign spacing
        res = []
        for i, line in enumerate(lines):
            lcnt = 0
            for w in line: lcnt += len(w)
            scnt = maxWidth - lcnt
            slot = len(line) - 1
            if slot > 0: base, extra = scnt // slot, scnt%slot
            # case: 1-word or last line
            # case other: first slot = scnt // slot + scnt%slot, other slot = scnt // slot
            tmp = ""
            for j, w in enumerate(line):
                if slot == 0:
                    tmp += w
                    tmp += " "*scnt
                elif i == len(lines) - 1:
                    if j < len(line) - 1:
                        tmp += w + " "
                        scnt -= 1
                    else: tmp += w
                else:
                    if j == len(line)-1: tmp += w
                    else: 
                        space = base + (1 if j < extra else 0)
                        tmp += w + " "*space
            
            if i == len(lines) - 1 and len(tmp) < maxWidth: tmp += " "*(maxWidth-len(tmp))
            res.append(tmp)
        return res


"""
Requirement:
1. each line has maxWidth characters
2. distribute ' ' evenly if possible; otherwise, more empty spaces at the left slot
3. last line: align to left w/n extra spaces between words
4. also left-align if only one word in a line

My Thought:
1. loop words: record specific word in each line by tracking letter cnt and basic 1 space between words
2. for each line, assign spaces
2.1 for one-word and last line, align left
"""