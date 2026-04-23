class Node:
    __slots__ = 'children', 'end'
    def __init__(self):
        self.children = {}
        self.end = False

class WordDictionary:
    def __init__(self):
        self.root = Node()

    def addWord(self, word: str) -> None:
        cur = self.root
        for w in word:
            if w not in cur.children:
                cur.children[w] = Node()
            cur = cur.children[w]
        cur.end = True

    def find(self, word: str, idx: int, node: Node) -> bool:
        # end case
        if len(word) == idx:
            return node.end
        
        # process
        cur = word[idx]
        # case: .
        if cur == '.':
            for n in node.children.values():
                if self.find(word, idx+1, n):
                    return True
            return False
        # case: letter
        else:
            if cur not in node.children:
                return False
            return self.find(word, idx+1, node.children[cur])
    
    def search(self, word: str) -> bool:
        return self.find(word, 0, self.root)    

# Your WordDictionary object will be instantiated and called as such:
# obj = WordDictionary()
# obj.addWord(word)
# param_2 = obj.search(word)