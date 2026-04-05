# One Iteration
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        # 滑动窗口依赖单调性, but nums[i] here can be positive / negative => prefix
        # subarray_sum = k = nums[:i] - nums[:j] while i >= j, so nums[:j] = nums[:i] - k
        prefix_cnt = { 0:1 }
        prefix = res = 0

        for n in nums:
            prefix += n
            if prefix - k in prefix_cnt: res += prefix_cnt[prefix - k]
            prefix_cnt[prefix] = 1 + (prefix_cnt[prefix] if prefix in prefix_cnt else 0)
        return res

# Two Iterations
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        # 滑动窗口依赖单调性, but nums[i] here can be positive / negative
        # Prefix Sum
        # 1. build prefix_sum
        prefix = [0]
        for n in nums: prefix.append(prefix[-1] + n)
        
        # 2. subsum_end - subsum_start = k -> subs_start = subs_end - k
        res = 0
        cnt = defaultdict(int)

        for p in prefix:
            if (p-k) in cnt: res += cnt[p-k]
            cnt[p] += 1

        return res