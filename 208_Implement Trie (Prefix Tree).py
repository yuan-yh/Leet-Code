class Node:
    __slots__ = 'children', 'end'
    def __init__(self):
        self.children = {}
        self.end = False

class Trie:
    def __init__(self):
        self.head = Node()

    def insert(self, word: str) -> None:
        cur = self.head
        for c in word:
            if c not in cur.children: cur.children[c] = Node()
            cur = cur.children[c]
        cur.end = True

    def find(self, word: str) -> int:
        cur = self.head
        for c in word:
            if c not in cur.children: return -1
            cur = cur.children[c]
        return 0 if cur.end else 1

    def search(self, word: str) -> bool:
        return self.find(word) == 0

    def startsWith(self, prefix: str) -> bool:
        return self.find(prefix) != -1


# Your Trie object will be instantiated and called as such:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)