# Edge case: len(word) > width
class Solution:
    def countLines(self, text: str, width: int):
        # Need to handle newlines & whitespace
        # 1. split paragraphs
        paragraphs = text.split("\n")

        cnt = 0
        for para in paragraphs:
            # 2. split words
            words = para.split()
            cnt += 1

            # 3. case: empty paragraphs vs contents
            if not words: continue

            cur = 0
            for word in words:
                # 4. case: first word in line || fill line || new line
                if cur == 0: cur += len(word)
                elif cur + 1 + len(word) <= width: cur += 1 + len(word)
                else:
                    cnt += 1
                    cur = len(word)

        return cnt