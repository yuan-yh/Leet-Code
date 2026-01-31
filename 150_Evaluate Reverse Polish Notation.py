class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stack = []

        for t in tokens:
            # case: '+', '-', '*', and '/'
            if t == '+': t = stack.pop() + stack.pop()
            elif t == '-': t = - stack.pop() + stack.pop()
            elif t == '*': t = stack.pop() * stack.pop()
            elif t == '/': 
                denominator = stack.pop()
                t = int(stack.pop() / denominator)
            
            stack.append(int(t))
        return stack.pop()