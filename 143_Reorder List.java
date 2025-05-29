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
    public void reorderList(ListNode head) {
        // 1. LC 876: find the middle of the list: slow
        ListNode fast = head, slow = head;
        while (fast != null && fast.next != null) {
            fast = fast.next.next;
            slow = slow.next;
        }
        // 2. LC 206: reverse the list starting from middle: new_reversed_head: prev
        ListNode cur = slow, prev = null, tmp;
        while (cur != null) {
            tmp = cur.next;
            cur.next = prev;
            prev = cur;
            cur = tmp;
        }
        // 3. repeatedly collect nodes from head->middle-1 & reverse tail->middle
        // ListNode vHead = new ListNode();
        ListNode tmp1, tmp2;
        // while (head != null && prev != null && head != prev && head.next != prev) {
        while (prev.next != null) {
            tmp1 = head.next;
            tmp2 = prev.next;
            head.next = prev;
            prev.next = tmp1;
            head = tmp1;
            prev = tmp2;
        }
    }
}