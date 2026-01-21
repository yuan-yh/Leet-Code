class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        # 想象你在路上行驶，最低点就是最低的谷底。 在當前谷底的位置必然要開始爬升，才能爬出低谷。
        start = tank = net = 0
        for i, (g, c) in enumerate(zip(gas, cost)):
            curCost = g - c
            tank += curCost
            net += curCost

            if tank < 0:
                # 最优起点 = 低谷的下一个位置
                start = i + 1
                tank = 0
        
        return start if net >= 0 else -1

# Method 2: loop
# class Solution:
#     def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
#         start = tank = net = 0
#         length = len(gas)

#         gas, cost = gas + gas, cost + cost

#         for i, (g, c) in enumerate(zip(gas, cost)):
#             curCost = g - c
#             tank += curCost
#             net += curCost

#             if tank < 0:
#                 start = i + 1
#                 tank = 0
        
#         return start if start < length else -1