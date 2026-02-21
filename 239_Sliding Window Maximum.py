# Method 1: record index - easier to handle duplicates
class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        # Monotonic stack: record idx in DESC for nums[i]
        q = deque()
        res = []

        for i, n in enumerate(nums):
            # case: cur >= tail: remove all smaller prefix then attach
            # case: cur < tail: attach
            while q and n >= nums[q[-1]]: q.pop()
            q.append(i)
            # window: record head when valid, then remove expired if head
            start = i - k + 1
            if start >= 0:
                res.append(nums[q[0]])
                if start == q[0]: q.popleft()
        return res

# # Method 2: record values - be careful for duplicates
# class Solution:
#     def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
#         # Use Deque to track valid max in the cur window
#         q = deque()
#         res = []

#         for i, n in enumerate(nums):
#             # Case: >= tail: pop until empty or until >= cur then attach
#             # Case: <= tail: attach
#             while q and q[-1] < n: q.pop()
#             q.append(n)
#             # Case: expire window start - matter if it is the head
#             start = i - k + 1
#             if start >= 0:
#                 res.append(q[0])
#                 if nums[start] == q[0]: q.popleft()

#         return res