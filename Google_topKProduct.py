# 1. not fixed k: prefix array
class ProductOfNumbers:
    def __init__(self):
        self.prefix = [1]  # prefix[0] = 1 (空乘积)
    
    def addNumber(self, num):
        """添加数字，更新前缀积"""
        if num == 0:
            # 遇到0，重置前缀积数组
            # 因为任何包含0的乘积都是0
            self.prefix = [1]
        else:
            self.prefix.append(self.prefix[-1] * num)
    
    def getProduct(self, k):
        """
        获取最近k个数字的乘积
        product(last k) = prefix[n] / prefix[n-k]
        """
        n = len(self.prefix)
        
        if k >= n:
            # 如果k大于等于当前数字数量
            # 说明在最近k个数字中包含了0（因为遇到0会重置）
            return 0
        
        return self.prefix[-1] // self.prefix[-k-1]

# 测试
obj = ProductOfNumbers()
obj.addNumber(3)    # [3]          prefix = [1, 3]
obj.addNumber(0)    # [3, 0]       prefix = [1] (重置)
obj.addNumber(2)    # [3, 0, 2]    prefix = [1, 2]
obj.addNumber(5)    # [3, 0, 2, 5] prefix = [1, 2, 10]
obj.addNumber(4)    # [...]        prefix = [1, 2, 10, 40]

print(obj.getProduct(2))  # 最近2个: 5*4 = 40
print(obj.getProduct(3))  # 最近3个: 2*5*4 = 40
print(obj.getProduct(4))  # 最近4个: 包含0 = 0


# 2. fixed k: deque to maintain the window
from collections import deque

class ProductOfNumbers:
    def __init__(self, k):
        """
        如果k是固定的，可以只维护k个数字的窗口
        k: 固定的窗口大小
        """
        self.k = k
        self.window = deque(maxlen=k)  # 自动维护大小
        self.product = 1
        self.has_zero = False
    
    def addNumber(self, num):
        """添加数字"""
        # 如果窗口满了，需要移除最老的数字
        if len(self.window) == self.k:
            old_num = self.window[0]  # 即将被移除的数字
            
            # 更新乘积：移除旧数字的影响
            if old_num == 0:
                # 重新计算整个窗口的乘积
                self.has_zero = False
                self.product = 1
                for n in list(self.window)[1:]:  # 除了第一个
                    if n == 0:
                        self.has_zero = True
                    self.product *= n
            else:
                self.product //= old_num
        
        # 添加新数字
        self.window.append(num)
        
        if num == 0:
            self.has_zero = True
        else:
            self.product *= num
    
    def getProduct(self, k=None):
        """获取最近k个数字的乘积"""
        if k is None:
            k = self.k
        
        if self.has_zero:
            return 0
        
        # 如果请求的k小于窗口大小
        if k < len(self.window):
            result = 1
            for i in range(len(self.window) - k, len(self.window)):
                result *= self.window[i]
            return result
        
        return self.product

# 测试（窗口大小为3）
obj = ProductOfNumbers(k=3)
obj.addNumber(2)
obj.addNumber(3)
obj.addNumber(4)
print(obj.getProduct())  # 2*3*4 = 24

obj.addNumber(5)  # 窗口现在是 [3,4,5]
print(obj.getProduct())  # 3*4*5 = 60