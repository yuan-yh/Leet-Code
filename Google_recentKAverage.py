"""
有一个data stream找到最新的K个元素的average，但是元素会一直更新，用queue就好。
follow-up：同样的data stream，但是要在最新的K个元素中去掉X个最大的元素然后求average。
楼主一开始说了个priority queue，面试官说不太efficiency，然后思考了一会儿用sortedList，压哨写完
"""
from collections import deque
from sortedcontainers import SortedList
from typing import List

class Solution:
    def __init__(self, k):
        self.q = deque()
        self.total = 0
        self.k = k
    
    def join(self, n):
        """添加新元素到数据流"""
        self.q.append(n)
        self.total += n
        if len(self.q) > self.k:
            self.total -= self.q.popleft()
    
    def topKAverage(self) -> float:  # 移除了 nums 参数,因为没用到
        """返回最近K个元素的平均值"""
        if len(self.q) == 0:
            return 0
        return self.total / len(self.q)  # 使用浮点除法
    
    def followup(self, x: int) -> float:
        """
        返回最近K个元素中去掉X个最大值后的平均值
        1. 获取最近k个元素
        2. 移除x个最大的元素
        3. 计算剩余元素的平均值
        """
        # 边界检查
        if x >= len(self.q) or len(self.q) == 0:
            return 0
        
        # 创建有序列表
        sl = SortedList()
        for num in self.q:  # 可以直接迭代 deque
            sl.add(num)  # 使用 add() 而不是 append()
        
        # 计算去掉x个最大值后的和
        tmptotal = 0
        for i in range(len(sl) - x):  # 只遍历前 (len-x) 个元素
            tmptotal += sl[i]
        
        # 除以剩余元素的数量
        return tmptotal / (len(self.q) - x)

# Version 2:
from sortedcontainers import SortedList
from collections import deque

class MovingAverageExcludeMax:
    def __init__(self, size, exclude):
        self.queue = deque()      # 维护窗口顺序
        self.sorted_list = SortedList()  # 维护排序
        self.size = size          # 窗口大小K
        self.exclude = exclude    # 要排除的最大值数量X
        self.sum = 0             # 所有元素的和
    
    def next(self, val):
        # 如果窗口已满,移除最旧的元素
        if len(self.queue) == self.size:
            old_val = self.queue.popleft()
            self.sorted_list.remove(old_val)
            self.sum -= old_val
        
        # 添加新元素
        self.queue.append(val)
        self.sorted_list.add(val)
        self.sum += val
        
        # 计算去掉X个最大值后的平均值
        if len(self.sorted_list) <= self.exclude:
            return 0  # 如果元素不够,返回0或特殊值
        
        # 计算要排除的最大值的和
        exclude_sum = sum(self.sorted_list[-(self.exclude):])
        valid_count = len(self.sorted_list) - self.exclude
        
        return (self.sum - exclude_sum) / valid_count