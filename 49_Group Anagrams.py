class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # sort each word in lexico order as key
        record = {}
        for s in strs:
            key = ''.join(sorted(s))
            if key not in record: record[key] = []
            record[key].append(s)
        
        res = []
        for _, val in record.items(): res.append(val)
        return res