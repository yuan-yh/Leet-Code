class SeatManager:
    def __init__(self, n: int):
        self.full = set()
        self.seats = []
        for i in range(1, n+1): heappush(self.seats, i)

    def reserve(self) -> int:
        # return the smallest idx available
        target = heappop(self.seats)
        self.full.add(target)
        return target

    def unreserve(self, seatNumber: int) -> None:
        self.full.remove(seatNumber)
        heappush(self.seats, seatNumber)


# Your SeatManager object will be instantiated and called as such:
# obj = SeatManager(n)
# param_1 = obj.reserve()
# obj.unreserve(seatNumber)