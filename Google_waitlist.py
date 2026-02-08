class Group:
    __slots__ = 'name', 'size', 'prev', 'next'
    def __init__(self, name="", size=inf):
        self.name = name
        self.size = size
        self.prev = None
        self.next = None

class Waitlist:
    def __init__(self):
        self.record = {}    # key: name, val: Group node
        self.head = Group()
        self.tail = Group()
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def join(self, name, size):
        if name not in self.record:
            newGroup = Group(name, size)
            # insert to tail & update record
            tmpt = self.tail.prev
            tmpt.next = newGroup
            newGroup.prev = tmpt
            newGroup.next = self.tail
            self.tail.prev = newGroup

            self.record[name] =  newGroup
    
    def delete(self, name):
        if name in self.record:
            target = self.record[name]
            # 1. break connection
            tprev, tnext = target.prev, target.next
            tprev.next = tnext
            tnext.prev = tprev
            # 2. del from hashmap
            del self.record[name]
    
    def find_first_match(self, table: int):
        cur = self.head.next
        while cur and cur.size > table:
            cur = cur.next
        return cur if cur else None