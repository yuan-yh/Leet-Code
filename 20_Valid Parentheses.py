class Solution:
    def isValid(self, s: str) -> bool:
        # Key Insight: dictionary + stack
        # 1. init parenthese record
        record = {'(': ')', '{': '}', '[': ']'}
        # 2. build stack while loop
        stack = []
        for c in s:
            if c in record: stack.append(record[c])
            elif not stack or c != stack.pop(): return False
        return len(stack) == 0