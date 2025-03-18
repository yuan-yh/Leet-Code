// Time complexity: O(1) for each put() and get() operation.
// Space complexity: O(n)

public class Node {
    int key;
    int value;
    Node prev;
    Node next;

    public Node(int key, int value) {
        this.key = key;
        this.value = value;
        this.prev = null;
        this.next = null;
    }
}

class LRUCache {
    private int capacity;
    private Map<Integer, Node> cache;
    private Node head;
    private Node tail;

    public LRUCache(int capacity) {
        this.capacity = capacity;
        this.cache = new HashMap<>();
        this.head = new Node(0, 0);
        this.tail = new Node(0, 0);
        this.head.next = this.tail;
        this.tail.prev = this.head;
    }

    private void remove(Node target) {
        if (target == null) return;
        Node tmpPrev = target.prev, tmpNext = target.next;
        if (tmpPrev != null) tmpPrev.next = tmpNext;
        if (tmpNext != null) tmpNext.prev = tmpPrev;
    }

    private void insert(Node target) {
        Node tmpHead = this.head.next;
        this.head.next = target;
        target.prev = this.head;
        target.next = tmpHead;
        tmpHead.prev = target;
    }
    
    public int get(int key) {
        if (cache.containsKey(key)) {
            Node target = cache.get(key);
            remove(target);
            insert(target);
            return target.value;
        }
        return -1;
    }
    
    public void put(int key, int value) {
        if (cache.containsKey(key)) remove(cache.get(key));
        Node newNode = new Node(key, value);
        insert(newNode);
        cache.put(key, newNode);
        if (cache.size() > capacity) {
            Node target = this.tail.prev;
            remove(target);
            cache.remove(target.key);
        }
    }
}