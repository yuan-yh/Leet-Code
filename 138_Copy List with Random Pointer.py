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
        # HashMap: key - original node, val - clone node (node.val cannot as key for duplicates)
        record = {}
        # 1. clone node
        tmp = head
        while tmp:
            if tmp not in record: record[tmp] = Node(tmp.val)
            tmp = tmp.next
        # 2. update next/random
        tmp = head
        while tmp:
            clone = record[tmp]
            if tmp.next: clone.next = record[tmp.next]
            if tmp.random: clone.random = record[tmp.random]
            tmp = tmp.next
        return record[head] if head else None