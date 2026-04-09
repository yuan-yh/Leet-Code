"""
# Definition for a Node.
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random
"""

class Solution:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        # 1. clone (original : clone)
        record = { None: None }
        cur = head

        while cur:
            ccur = Node(cur.val)
            record[cur] = ccur
            cur = cur.next
        # 2. connect
        cur = head
        while cur:
            clone = record[cur]
            clone.next = record[cur.next]
            clone.random = record[cur.random]
            cur = cur.next
        return record[head]