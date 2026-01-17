class Solution:
    def hammingWeight(self, n: int) -> int:
        cnt = 0
        while n:
            cnt += n & 1    # Bitwise AND: & 比较两个数的最后一位，都为 1 时结果才为 1
            n >>= 1         # 右移赋值: >> 是右移运算符，所有位向右移动，最右边的位被丢弃
        return cnt