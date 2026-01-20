"""
# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
"""

from typing import Optional
class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        # queue + hashmap/dictionary
        if not node: return None
        
        record = defaultdict(list)          # Key: val; Value: new_node
        q = deque([node])                   # origin_node to do processed

        head = Node(node.val)
        record[node.val] = head

        while q:
            org = q.popleft()
            copy = record[org.val]

            for n in org.neighbors:
                if n.val not in record:
                    record[n.val] = Node(n.val)
                    q.append(n)
                copy.neighbors.append(record[n.val])

        return head