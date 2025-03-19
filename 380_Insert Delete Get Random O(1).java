// Time complexity: O(1) for each function call.
// Space complexity: O(n)

class RandomizedSet {
    private Map<Integer, Integer> numMap;
    private List<Integer> nums;
    private Random rand;

    public RandomizedSet() {
        this.numMap = new HashMap<>();
        this.nums = new ArrayList<>();
        this.rand = new Random();
    }
    
    public boolean insert(int val) {
        if (numMap.containsKey(val)) return false;
        numMap.put(val, nums.size());
        nums.add(val);
        return true;
    }
    
    public boolean remove(int val) {
        if (!numMap.containsKey(val)) return false;
        int index = numMap.get(val), replaceVal = nums.get(nums.size() - 1);
        nums.set(index, replaceVal);
        nums.remove(nums.size() - 1);
        numMap.put(replaceVal, index);
        numMap.remove(val);
        return true;
    }
    
    public int getRandom() {
        return nums.get(rand.nextInt(nums.size()));
    }
}

/**
 * Your RandomizedSet object will be instantiated and called as such:
 * RandomizedSet obj = new RandomizedSet();
 * boolean param_1 = obj.insert(val);
 * boolean param_2 = obj.remove(val);
 * int param_3 = obj.getRandom();
 */