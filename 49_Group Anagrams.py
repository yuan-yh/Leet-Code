class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # HashMap: key-sorted_str, val-[str]
        record = defaultdict(list)

        for s in strs:
            # 1. sort as the key
            key = ''.join(sorted(s))
            # 2. append to record[sorted]
            record[key].append(s)

        return list(record.values())