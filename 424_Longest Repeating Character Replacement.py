# Key insight: window - max_repeat_cnt_in_the_window <= k

class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        # Key insight: window - max_history_repeat_cnt_in_the_window <= k
        record = [0] * 26
        l = max_cnt = 0

        for r in range(len(s)):
            # 1. update cur_letter cnt
            cur = ord(s[r]) - ord('A')
            record[cur] += 1

            # 2. update max_cnt in the valid window history
            max_cnt = max(max_cnt, record[cur])
            # 3. shift the left boundary if window not satisfied
            if (r - l + 1) - max_cnt > k:
                record[ord(s[l]) - ord('A')] -= 1
                l += 1
            # 4. Now [l : r] maintains the max length of valid window in history
        
        return len(s) - l