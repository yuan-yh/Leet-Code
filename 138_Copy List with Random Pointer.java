// 时间复杂度：O(n)，其中 n 是链表的长度。
// 空间复杂度：O(1)。返回值不计入。

/*
// Definition for a Node.
class Node {
    int val;
    Node next;
    Node random;

    public Node(int val) {
        this.val = val;
        this.next = null;
        this.random = null;
    }
}
*/

// Method 1: in-place insertion
/*
// Definition for a Node.
class Node {
    int val;
    Node next;
    Node random;

    public Node(int val) {
        this.val = val;
        this.next = null;
        this.random = null;
    }
}
*/

class Solution {
    public Node copyRandomList(Node head) {
        // 1. in-place insertion
        for (Node n = head; n != null; n = n.next.next) {
            n.next = new Node(n.val, n.next);
        }
        // 2. update random
        for (Node n = head; n != null; n = n.next.next) {
            if (n.random != null) n.next.random = n.random.next;
        }
        // 3. remove original nodes to update next
        Node vHead = new Node(0);
        Node cur = vHead;

        for (Node n = head; n != null; n = n.next) {
            Node clone = n.next;
            cur.next = clone;
            cur = cur.next;
            n.next = n.next.next;
        }

        return vHead.next;
    }
}

// // Method 2: Hashmap
// class Solution {
//     public Node copyRandomList(Node head) {
//         // 1. HashMap
//         Map<Node, Node> record = new HashMap<>();
//         record.put(null, null);

//         // 2. clone nodes
//         Node org = head, clone;
//         while (org != null) {
//             record.put(org, new Node(org.val));
//             org = org.next;
//         }
        
//         // 3. update next & random
//         org = head;
//         while (org != null) {
//             clone = record.get(org);
//             clone.next = record.get(org.next);
//             clone.random = record.get(org.random);
//             org = org.next;
//         }

//         return record.get(head);
//     }
// }