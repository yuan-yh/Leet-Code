class RecentCounter:
    # It is guaranteed that every call to ping uses a strictly larger value of t than the previous call.
    # Based on this given statement, maintain a sliding window / valid queue
    def __init__(self):
        self.record = deque()

    def ping(self, t: int) -> int:
        self.record.append(t)
        while self.record[0] < t-3000: self.record.popleft()
        return len(self.record)


# Your RecentCounter object will be instantiated and called as such:
# obj = RecentCounter()
# param_1 = obj.ping(t)