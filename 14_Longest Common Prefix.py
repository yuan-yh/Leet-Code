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
        res = ""
        cur = head

        while cur:
            # check for end or only one children
            if cur.end or len(cur.children) > 1: break

            key = next(iter(cur.children))      # iter() 转成迭代器, next() 获取第一个元素
            res += key
            cur = cur.children[key]

        return res