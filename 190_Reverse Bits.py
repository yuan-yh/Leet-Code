class Solution:
    def reverseBits(self, n: int) -> int:
        res = 0
        # reverse into a 32 bits signed integer
        for i in range(32):
            # 1. append one 0 to the end of res / res右边补 1 个 0
            res <<= 1
            # 2. extract the last digit of n, then update the end of res w/ tail
            res += n & 1
            # 3. discard the tail of n / n丢弃最右边 1 位
            n >>= 1
        return res