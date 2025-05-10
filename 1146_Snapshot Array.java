class SnapshotArray {
    int snapId = 0;
    // TreeMap<快照ID, 该位置的值>
    TreeMap<Integer, Integer>[] history;

    public SnapshotArray(int length) {
        history = new TreeMap[length];
        // init
        for (int i = 0; i < length; i++) {
            history[i] = new TreeMap<>();
            history[i].put(0, 0);
        }
    }
    
    public void set(int index, int val) {
        history[index].put(snapId, val);
    }
    
    public int snap() {
        // 先返回 snapId 的当前值，然后再对 snapId 加 1 
        return snapId++;
    }
    
    public int get(int index, int snap_id) {
        // floorEntry: 返回小于或等于给定键的最大键对应的键值对（Map.Entry）
        return history[index].floorEntry(snap_id).getValue();
    }
}

/**
 * Your SnapshotArray object will be instantiated and called as such:
 * SnapshotArray obj = new SnapshotArray(length);
 * obj.set(index,val);
 * int param_2 = obj.snap();
 * int param_3 = obj.get(index,snap_id);
 */