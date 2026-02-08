class Solution:
    def wordsTyping(self, sentence: List[str], rows: int, cols: int) -> int:
        # 1. connect sentences into text for loop
        text = " ".join(sentence) + " "
        ptr = 0

        # 2. loop each row & update ptr by cols
        for r in range(rows):
            ptr += cols
            # case: newStart points to space (skip & start from word) || word (backtrack to space then skip space)
            while text[ptr % len(text)] != " ": ptr -= 1
            ptr += 1

        return ptr // len(text)