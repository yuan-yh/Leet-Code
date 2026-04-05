
class Node:
    __slots__ = "key", "val", "prev", "next"

    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None
    
class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.record = {}
        self.head = Node()
        self.tail = Node()

        self.head.next = self.tail
        self.tail.prev = self.head

    def breakConnect(self, node):
        pn, nn = node.prev, node.next
        pn.next = nn
        nn.prev = pn
    
    def insertFront(self, node):
        th = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = th
        th.prev = node
    
    def get(self, key: int) -> int:
        # 1. fetch node
        if key not in self.record: return -1
        target = self.record[key]
        # 2. break connection
        self.breakConnect(target)
        # 3. insert front
        self.insertFront(target)
        return target.val

    def put(self, key: int, value: int) -> None:
        # 1. fetch existing node & update val
        if key in self.record: 
            target = self.record[key]
            target.val = value
            self.breakConnect(target)
        # 2. create new node
        else: 
            target = Node(key, value)
            self.record[key] = target
        # 3. delete if above capacity
        if len(self.record) > self.capacity:
            toDel = self.tail.prev
            self.breakConnect(toDel)
            del self.record[toDel.key]
        # 4. insert front
        self.insertFront(target)


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)