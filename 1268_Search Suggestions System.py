class Node:
    __slots__ = 'children', 'minIdx', 'maxIdx'

    def __init__(self):
        self.children = {}
        self.minIdx = inf
        self.maxIdx = -inf

class Solution:
    def suggestedProducts(self, products: List[str], searchWord: str) -> List[List[str]]:
        # 1. sort products in lexico order
        products.sort()

        # 2. build Trie (record min/max_idx of sorted products matching this prefix)
        thead = Node()

        for i, p in enumerate(products):
            cur = thead
            
            for c in p:
                if c not in cur.children: cur.children[c] = Node()
                cur = cur.children[c]

                cur.minIdx = min(cur.minIdx, i)
                cur.maxIdx = max(cur.maxIdx, i)
        
        # 3. loop searchw in Trie
        res = []
        cur = thead

        for sw in searchWord:
            curPath = []

            # 4. Case: sw not found in Trie or out of Trie scope
            if cur and sw in cur.children:
                cur = cur.children[sw]

                for i in range(cur.minIdx, min(cur.maxIdx+1, cur.minIdx+3)):
                    curPath.append(products[i])
            else: cur = None
            
            res.append(curPath)
        return res