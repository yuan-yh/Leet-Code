class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        # look for the window in s2 that qualifies for cnt1
        cnt1 = Counter(s1)
        cnt2 = defaultdict(int)
        left = 0

        for r, c in enumerate(s2):
            # case 1: c not in cnt1
            if c not in cnt1:
                cnt2.clear()
                left = r + 1
                continue
            
            cnt2[c] += 1
            # case 2: c count in cnt2 exceeds the count in cnt1
            while cnt2[c] > cnt1[c]:
                cnt2[s2[left]] -= 1
                left += 1
            # case 3: window length match
            if r - left + 1 == len(s1): return True
        
        return False