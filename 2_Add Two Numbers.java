// Time complexity: O(m+n)
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
    public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        ListNode vHead = new ListNode();
        ListNode tmp = vHead;
        int carryOn = 0;

        while (l1 != null || l2 != null || carryOn > 0) {
            if (l1 != null) {
                carryOn += l1.val;
                l1 = l1.next;
            }
            if (l2 != null) {
                carryOn += l2.val;
                l2 = l2.next;
            }
            tmp.next = new ListNode(carryOn % 10);
            carryOn = carryOn / 10;
            tmp = tmp.next;
        }

        return vHead.next;
    }
}