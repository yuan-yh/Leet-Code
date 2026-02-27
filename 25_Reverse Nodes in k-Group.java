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
    public ListNode reverseKGroup(ListNode head, int k) {
        ListNode vHead = new ListNode(0, head);
        ListNode cur = vHead;

        // 1. record length
        int length = 0;
        while (cur.next != null) {
            length += 1;
            cur = cur.next;
        }

        // 2. calculate reverse_cnt
        int cnt = length / k;

        // 3. reverse
        cur = vHead;
        for (int i = 0; i < cnt; i++) {
            ListNode tail = cur.next, prev = null, tmp;
            for (int j = 0; j < k; j++) {
                tmp = cur.next;
                cur.next = cur.next.next;
                tmp.next = prev;
                prev = tmp;
            }
            // 4. shift cur
            tail.next = cur.next;
            cur.next = prev;
            cur = tail;
        }

        return vHead.next;
    }
}