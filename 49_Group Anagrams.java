// 时间复杂度：O(nmlogm)，其中 n 为 strs 的长度，m 为 strs[i] 的长度。
//  每个字符串排序需要 O(mlogm) 的时间，有 n 个字符串，所以总的时间复杂度为 O(nmlogm)。
// 空间复杂度：O(nm)。

class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> record = new HashMap<>();

        for (String s : strs) {
            // 1. sort as key
            char[] sArray = s.toCharArray();
            Arrays.sort(sArray);
            String key = new String(sArray);
            // 2. update hashmap
            record.putIfAbsent(key, new ArrayList<>());
            record.get(key).add(s);
        }
        return new ArrayList<>(record.values());
    }
}