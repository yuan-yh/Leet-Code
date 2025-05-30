// Time complexity: O(n)
// Space complexity: O(1)

/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode() {}
 *     ListNode(int val) { this.val = val; }
 *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
class Solution {
    public ListNode removeNthFromEnd(ListNode head, int n) {
        // the fast & slow ptr is 'n' away
        ListNode fast = head, slow = head;
        // 1. ensure the fast ptr is 'n' ahead
        while (n > 0) {
            fast = fast.next;
            n--;
        }
        // 2. remove the slow.next node
        // case: remove the head node
        if (fast == null) return head.next;
        // case: remove the middle / tail node
        while (fast.next != null) {
            slow = slow.next;
            fast = fast.next;
        }
        slow.next = slow.next.next;
        return head;
    }
}