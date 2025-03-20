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

/**
 * Follow-up:
 * 如果一个链表是逆序的，另一个链表是正序的，但你不能使用列表来存储中间结果，如何解决这个问题？
 * 
 * Solution: 
 * 1. 反转正序链表：首先将正序链表反转，使其变为逆序链表。
 * See 206. Reverse Linked List
 * 2. 使用原始问题的解法：现在两个链表都是逆序的，我们可以直接使用原始问题的解法来相加两个链表。
 * 3. 反转结果链表：最后，将结果链表反转，使其变为正序链表。
 */

public class Solution {
    public ListNode reverseList(ListNode head) {
        ListNode prev = null;
        ListNode curr = head;

        while (curr != null) {
            ListNode temp = curr.next;
            curr.next = prev;
            prev = curr;
            curr = temp;
        }
        return prev;
    }
}