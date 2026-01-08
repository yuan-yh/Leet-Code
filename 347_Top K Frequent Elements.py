# Method 1: Bucket Sort - O(n)
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # 1. count letter frequency
        count = Counter(nums)
        # 2. create len(nums) buckets and fill
        bucket = [[] for _ in range(len(nums) + 1)]
        for i, cnt in count.items():
            bucket[cnt].append(i)
        # 3. loop backwards
        res = []
        for i in range(len(nums), -1, -1):
            res += bucket[i]
            if len(res) == k: break
        return res
        
# # Method 2: Heap - O(n log(n))
# class Solution:
#     def topKFrequent(self, nums: List[int], k: int) -> List[int]:
#         # 1. count letter
#         count = Counter(nums)
#         # 2. loop through counter while maintain a heap w/ size k
#         minh = []
#         for i, cnt in count.items():
#             if len(minh) < k: heappush(minh, (cnt, i))
#             elif minh[0][0] < cnt:
#                 heappop(minh)
#                 heappush(minh, (cnt, i))
#         # 3. return the heap with val only
#         return [i for cnt, i in minh]