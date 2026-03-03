# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

ListNode.__lt__ = lambda a, b : a.val < b.val

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        min_heap = []
        vHead = cur = ListNode()

        # 1. enqueue all heads
        for head in lists: 
            if head:
                heappush(min_heap, head)

        # 2. pop the min value, record & enqueue if has next
        while min_heap:
            tmp = heappop(min_heap)

            cur.next = tmp
            cur = cur.next

            if tmp.next: 
                heappush(min_heap, tmp.next)
        return vHead.next