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

# One Iteration
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        # 滑动窗口依赖单调性, but nums[i] here can be positive / negative
        # 1. maintain prefix_sum
        # 2. subsum_end - subsum_start = k -> subs_start = subs_end - k
        res = prefix = 0
        cnt = defaultdict(int)
        cnt[0] = 1

        for n in nums:
            prefix += n
            res += cnt[prefix - k]
            cnt[prefix] += 1

        return res