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
    public ListNode reverseBetween(ListNode head, int left, int right) {
        // edge case: same l/r = no swap
        if (left == right) return head;

        ListNode vHead = new ListNode(0, head);
        ListNode tmp = vHead;
        // vHead -> left-1 -> right -> swap -> left -> right + 1
        // 1. iterate, stop when find left, record pointers to left & left-1
        int index = 0;
        while (index < left - 1) {
            tmp = tmp.next;
            index ++;
        }
        ListNode leftward = tmp, leftPtr = tmp.next;

        // 2. reverse, stop when find and reverse right, record pointers to right & right+1
        ListNode prev = null, cur = leftPtr;
        index = left;
        while (index <= right) {
            tmp = cur.next;
            cur.next = prev;
            prev = cur;
            cur = tmp;
            index ++;
        }
        // 3. connect
        leftward.next = prev;
        leftPtr.next = cur;
        // 4. return head
        return vHead.next;
    }
}