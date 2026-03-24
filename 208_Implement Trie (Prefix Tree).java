class Node {
    Map<Character, Node> children;
    Boolean end;

    public Node() {
        this.children = new HashMap<>();
        this.end = false;
    }
}

class Trie {
    private Node head;

    public Trie() { this.head = new Node(); }
    
    public void insert(String word) {
        Node cur = this.head;
        for (Character c : word.toCharArray()) {
            if (!cur.children.containsKey(c)) cur.children.put(c, new Node());
            cur = cur.children.get(c);
        }
        cur.end = true;
    }
    
    private int find(String word) {
        Node cur = this.head;
        for (Character c : word.toCharArray()) {
            if (!cur.children.containsKey(c)) return -1;
            cur = cur.children.get(c);
        }
        return cur.end ? 1 : 0;
    }

    public boolean search(String word) { return find(word) == 1; }
    
    public boolean startsWith(String prefix) { return find(prefix) != -1; }
}

/**
 * Your Trie object will be instantiated and called as such:
 * Trie obj = new Trie();
 * obj.insert(word);
 * boolean param_2 = obj.search(word);
 * boolean param_3 = obj.startsWith(prefix);
 */