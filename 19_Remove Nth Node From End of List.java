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
        ListNode vHead = new ListNode(0, head);

        ListNode fast = vHead, slow = vHead;

        // 1. shift fast n steps ahead
        for (int i = 0; i < n; i++) fast = fast.next;

        // 2. shift together until tail
        while (fast.next != null) {
            fast = fast.next;
            slow = slow.next;
        }

        // 3. delete node
        slow.next = slow.next.next;

        return vHead.next;
    }
}