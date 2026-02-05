class Solution:
    def decodeString(self, s: str) -> str:
        # Stack
        stack = []
        res = ""
        cnt = 0
        
        for c in s:
            # case: digit, brackets, letter
            if c.isdigit(): cnt = cnt * 10 + int(c)
            elif c.isalpha(): res += c
            elif c == '[':
                stack.append(res)
                stack.append(cnt)
                res = ""
                cnt = 0
            else:
                prevCnt = stack.pop()
                res *= prevCnt
                res = stack.pop() + res
        
        return res