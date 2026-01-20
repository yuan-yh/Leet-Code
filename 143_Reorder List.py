# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        """
        Do not return anything, modify head in-place instead.
        """
        # 1. find median (the last of left half)
        fast, slow = head, head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        
        right = slow.next
        
        # 2. break the connection between left and right
        slow.next = None
        left = head
        
        # 3. reverse right
        def reverse(node) -> Optional[ListNode]:
            vHead = ListNode()
            while node:
                tmp = node.next
                node.next = vHead.next
                vHead.next = node
                node = tmp
            return vHead.next
        
        right = reverse(right)
        
        # 4. append l/r repeatedly - end case: invalid r as l always appended to the cur valid tail already
        while right:
            n1, n2 = left.next, right.next
            left.next = right
            right.next = n1
            left, right = n1, n2