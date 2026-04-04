class Solution:
    def isValid(self, s: str) -> bool:
        # 1. init parentheses relationship
        relation = {'(': ')', '{': '}', '[': ']'}
        # 2. maintain stack
        stack = []

        for c in s:
            if c in relation: stack.append(relation[c])
            elif not stack or c != stack.pop(): return False
        return not stack