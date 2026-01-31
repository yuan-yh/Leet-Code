# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        vHead = cur = ListNode()
        addson = 0

        while addson > 0 or l1 or l2:
            if l1: 
                addson += l1.val
                l1 = l1.next
            if l2: 
                addson += l2.val
                l2 = l2.next
            
            cur.next = ListNode(addson % 10)
            cur = cur.next
            addson //= 10

        return vHead.next