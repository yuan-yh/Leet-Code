class Solution:
    def calculate(self, s: str) -> int:
        # Stack - track sign and elements outside the parentheses
        curRes, curDigit, sign = 0, 0, 1
        stack = []

        for c in s:
            # digits, '+', '-', '(', ')', and ' '
            if c.isdigit(): curDigit = curDigit*10 + int(c)
            elif c == '+' or c == '-':
                # process the left component
                curRes += sign * curDigit
                curDigit = 0
                sign = 1 if c == '+' else -1
            elif c == '(':
                # record the left component w/ its sign into the stack
                stack.append((curRes, sign))
                curRes, curDigit, sign = 0, 0, 1
            elif c == ')':
                # process the right component (w/in the parentheses), pop the left component w/ sign, process & update curRes
                curRes += curDigit * sign
                prevRes, prevSign = stack.pop()
                curRes = prevRes + prevSign * curRes
                curDigit, sign = 0, 1

        curRes += curDigit * sign
        return curRes