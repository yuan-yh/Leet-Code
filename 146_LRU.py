class Node:
    __slots__ = 'key', 'val', 'prev', 'next'
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.record = {}            # key: node.key, val: node
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def delete(self, node):
        pnode, nnode = node.prev, node.next
        pnode.next = nnode
        nnode.prev = pnode
    
    def insert(self, node):
        phead = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = phead
        phead.prev = node
    
    def get(self, key: int) -> int:
        if key not in self.record: return -1
        target = self.record[key]
        self.delete(target)
        self.insert(target)
        return target.val

    def put(self, key: int, value: int) -> None:
        if key in self.record:
            target = self.record[key]
            target.val = value
            self.delete(target)
        else: 
            target = Node(key, value)
            self.record[key] = target
        
        self.insert(target)

        if len(self.record) > self.capacity:
            expire = self.tail.prev
            self.delete(expire)
            del self.record[expire.key]


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)