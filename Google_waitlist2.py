class Group:
    def __init__(self, name="", size=0):
        self.name = name
        self.size = size
        self.prev = None
        self.next = None

class Waitlist:
    # join or out
    # check the queue
    # check the top or bottom k
    def __init__(self):
        self.record = {}
        self.head = Group()
        self.tail = Group()
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def breakConnect(self, group):
        pg, ng = group.prev, group.next
        pg.next = ng
        ng.prev = pg
    
    def join(self, name, size):
        if name in self.record: return

        target = Group(name, size)
        ttail = self.tail.prev
        ttail.next = target
        target.prev = ttail
        target.next = self.tail
        self.tail.prev = target
        self.record[name] = target
    
    def leave(self, name):
        if name not in self.record: return
        target = self.record[name]
        self.breakConnect(target)
        del self.record[name]

    def check_top(self, k):
        res = []
        cur = self.head.next
        k = min(k, len(self.record))
        for _ in range(k):
            res.append(cur.name)
            cur = cur.next
        return res

    def check_bottom(self, k):
        res = []
        cur = self.tail.prev
        k = min(k, len(self.record))
        for _ in range(k):
            res.append(cur.name)
            cur = cur.prev
        return res