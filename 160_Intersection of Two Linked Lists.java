// 时间复杂度：O(m+n)，其中 m 是第一条链表的长度，n 是第二条链表的长度。除了交点，每个节点会被指针 p 访问至多一次，每个节点会被指针 q 访问至多一次。
// 空间复杂度：O(1)。


/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode(int x) {
 *         val = x;
 *         next = null;
 *     }
 * }
 */
public class Solution {
    public ListNode getIntersectionNode(ListNode headA, ListNode headB) {
        ListNode p1 = headA, p2 = headB;

        while (p1 != p2) {
            p1 = (p1 != null) ? p1.next : headB;
            p2 = (p2 != null) ? p2.next : headA;
        }

        return p1;
    }
}