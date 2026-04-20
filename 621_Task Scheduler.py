class Solution:
    # Method 1: track the gap time for the most-frequent task only
    # Ignore: too complicated
    # Core Idea: max(len(tasks), (max_freq - 1) * (n + 1) + num_max)
    
    # Method 2: simulate every time
    def leastInterval(self, tasks: List[str], n: int) -> int:
        # 1. count frequency
        count = Counter(tasks)
        # 2. push into max-heap (-freq)
        max_heap = [-f for f in count.values()]
        heapify(max_heap)
        # 3. init q to track cool-time (available_time, -freq)
        q = deque()
        # 4. simulation
        time = 0
        while max_heap or q:
            time += 1
            # 5. release completed cool_down task
            if q and q[0][0] <= time: heappush(max_heap, q.popleft()[1])
            # 6. process task if available
            if max_heap:
                curf = heappop(max_heap)
                if curf + 1 != 0: q.append((time + n + 1, curf + 1))
        return time