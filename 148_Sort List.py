# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def findMiddle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = fast = head
        while fast and fast.next:
            pre = slow
            slow = slow.next
            fast = fast.next.next
        pre.next = None
        return slow
    
    def merge(self, left: Optional[ListNode], right: Optional[ListNode]) -> Optional[ListNode]:
        vHead = cur = ListNode()

        while left and right:
            if left.val < right.val:
                cur.next = left
                left = left.next
            else:
                cur.next = right
                right = right.next
            cur = cur.next
        
        cur.next = left if left else right
        return vHead.next

    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # 0. case: <= 1 node
        if not (head and head.next): return head
        # 1. divide: find middle & split into two halves
        right = self.findMiddle(head)
        left = head

        # 2. sort
        left = self.sortList(left)
        right = self.sortList(right)

        # 3. merge / conquer
        return self.merge(left, right)
