class Node:
    __slots__ = "children", "end"
    def __init__(self):
        self.children = {}
        self.end = False

class Trie:

    def __init__(self):
        self.head = Node()

    def insert(self, word: str) -> None:
        cur = self.head
        for w in word:
            if w not in cur.children:
                cur.children[w] = Node()
            cur = cur.children[w]
        cur.end = True

    def find(self, word: str) -> int:
        cur = self.head
        for w in word:
            if w not in cur.children:
                return -1
            cur = cur.children[w]
        return 1 if cur.end else 0
    
    def search(self, word: str) -> bool:
        return self.find(word) == 1

    def startsWith(self, prefix: str) -> bool:
        return self.find(prefix) >= 0


# Your Trie object will be instantiated and called as such:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)