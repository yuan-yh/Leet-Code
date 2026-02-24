// Time complexity: O(n)
// Space complexity: O(1)

// head -> cycle entry: distance a
// cycle entry -> fast/slow ptr meet: distance b
// fast/slow ptr meet -> cycle entry: distance c
// therefore, cycle length = b + c

// case 1: when fast / slow ptr meet
// fast moves: a + b + (b + c)*k, k is an integer
// slow moves: a + b
// Given the fast ptr moves twice as the slow ptr: 
//      2*(a + b) = a + b + (b + c)*k
//      2*(a + b) - (a + b) - (b + c) = (b + c)*(k - 1)
//      a - c = (b + c)*(k - 1)

// case 2: have a new ptr to head after they meet, then have both start to move
// when slow reaches the cycle entry, the new ptr is (a-c) away from the entry, which is proportional to the cycle length
// therefore, if both keep iterating, they will meet at the cycle entry

/**
 * Definition for singly-linked list.
 * class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode(int x) {
 *         val = x;
 *         next = null;
 *     }
 * }
 */
/**
 * Definition for singly-linked list.
 * class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode(int x) {
 *         val = x;
 *         next = null;
 *     }
 * }
 */
public class Solution {
    public ListNode detectCycle(ListNode head) {
        ListNode fast = head, slow = head;

        while (fast != null && fast.next != null) {
            fast = fast.next.next;
            slow = slow.next;

            if (fast == slow) {
                while (head != slow) {
                    slow = slow.next;
                    head = head.next;
                }
                return head;
            }
        }

        return null;
    }
}