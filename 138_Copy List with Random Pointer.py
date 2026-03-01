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
        record = {}
        record[None] = None
        
        # 1. clone nodes
        org = head
        while org:
            record[org] = Node(org.val)
            org = org.next
        
        # 2. update next & random
        org = head
        while org:
            clone = record[org]
            clone.next = record[org.next]
            clone.random = record[org.random]
            org = org.next

        return record[head]