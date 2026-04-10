class Solution:
    def isValid(self, s: str) -> bool:
        MAPPINGS = {'(': ')', '[': ']', '{': '}'}
        q = deque()

        for c in s:
            if c in MAPPINGS: q.append(MAPPINGS[c])
            elif not q or q.pop() != c: return False
        return not q