# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        # 1. record length
        length = 0
        vHead = cur = ListNode(0, head)
        while cur.next:
            length += 1
            cur = cur.next
        
        # 2. reverse (length // k) times
        revCnt = length // k
        beforeTail, afterTail, rprev, rcur = vHead, head, None, head
        for _ in range(revCnt):
            for _ in range(k):
                tmp = rcur.next
                rcur.next = rprev
                rprev = rcur
                rcur = tmp
            # 3. connect with before-cur-reverse part (beforeTail) and the after part (cur)
            beforeTail.next = rprev
            afterTail.next = rcur
            # 4. update variables
            beforeTail, afterTail, rprev, rcur = afterTail, rcur, None, rcur
        
        return vHead.next