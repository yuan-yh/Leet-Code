class TimeMap:
    def __init__(self):
        # Timestamp w/ corresponding value is attached in ASC order
        self.record = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        if key not in self.record: self.record[key] = []
        self.record[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        # Edge case: no key || no value at or before the timestamp
        if key not in self.record: return ""

        tmp = self.record[key]
        l, r = -1, len(tmp) - 1     # (l, r]

        while l < r:
            m = (l + r + 1) >> 1
            if tmp[m][0] == timestamp: return tmp[m][1]
            elif tmp[m][0] < timestamp: l = m
            else: r = m - 1
        
        return tmp[l][1] if l >= 0 else ""


# Your TimeMap object will be instantiated and called as such:
# obj = TimeMap()
# obj.set(key,value,timestamp)
# param_2 = obj.get(key,timestamp)