# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        # 1. calculate length & local the tail node
        tail = cur = head
        length = 0
        while cur:
            tail = cur
            length += 1
            cur = cur.next
        
        # 2. short-cut: empty or only ONE node or k % length == 0
        if length <= 1 or k % length == 0: return head

        # 3. loop to the break point: length - k % length
        back = length - (k % length)

        # 4. re-attach: back+1_to_tail + head_to_back
        tmp = head
        for _ in range(back-1): tmp = tmp.next

        newHead = tmp.next
        tmp.next = None
        tail.next = head
        return newHead