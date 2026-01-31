class Solution:
    def isHappy(self, n: int) -> bool:
        record = set([n])

        while n > 1:
            tmp = 0
            while n != 0:
                tmp += (n % 10) ** 2
                n //= 10
            n = tmp
            if n in record: return False
            record.add(n)
        
        return n == 1   # 2 exit cases: n = 0 or n = 1