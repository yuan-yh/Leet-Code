class Node:
    __slots__ = "children", "end"
    def __init__(self):
        self.children = {}
        self.end = False

class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        # 1. build Trie
        head = Node()
        for s in strs:
            cur = head
            for c in s:
                if c not in cur.children:
                    cur.children[c] = Node()
                cur = cur.children[c]
            cur.end = True
        # 2. traverse
        cur = head
        for i, c in enumerate(strs[0]):
            if len(cur.children) > 1 or cur.end: return strs[0][:i]
            cur = cur.children[c]
        return strs[0]