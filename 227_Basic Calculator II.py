class Solution:
    def calculate(self, s: str) -> int:
        # Stack: */ have higher priority than +-, so process them first
        # For -, just convert the sign for next num
        stack = []
        prevOper = '+'
        num = 0

        for i, c in enumerate(s):
            # all possible cases: digit+-*/
            if c.isdigit(): num = num * 10 + int(c)
            # process the previous operation
            if i == len(s) - 1 or c in "+-*/":
                if prevOper == '*': stack.append(num * stack.pop())
                # Python: -3//2 = -2 -> （向负无穷方向取整）cannot use directly -> int(-3/2)
                elif prevOper == '/': 
                    top = stack.pop()
                    if top < 0: stack.append(int(top / num))
                    else: stack.append(top // num)
                elif prevOper == '-': stack.append(-num)
                elif prevOper == '+': stack.append(num)

                prevOper = c
                num = 0

        return sum(stack)