# 1. backtracking
def count_winning_combinations_backtracking(state_votes, target):
    """
    使用回溯法计算能赢得选举的州组合数量
    
    参数:
    state_votes: list[int] - 每个州的选举人票数
    target: int - 赢得选举所需的最小票数
    
    返回:
    int - 能达到或超过目标票数的组合数量
    """
    def backtrack(index, current_votes):
        # 基础情况:如果当前票数已经达到目标
        if current_votes >= target:
            return 1
        
        # 基础情况:如果已经考虑完所有州
        if index >= len(state_votes):
            return 0
        
        # 选择1: 不选择当前州
        count = backtrack(index + 1, current_votes)
        
        # 选择2: 选择当前州
        count += backtrack(index + 1, current_votes + state_votes[index])
        
        return count
    
    return backtrack(0, 0)


# 测试
state_votes = [3, 5, 7, 10, 15]  # 示例:5个州的选举人票数
target = 20  # 需要20票才能赢

result = count_winning_combinations_backtracking(state_votes, target)
print(f"能赢得选举的组合数量: {result}")

# 2. DP
def count_winning_combinations_dp(state_votes, target):
    """
    使用动态规划计算能赢得选举的州组合数量
    
    参数:
    state_votes: list[int] - 每个州的选举人票数
    target: int - 赢得选举所需的最小票数
    
    返回:
    int - 能达到或超过目标票数的组合数量
    """
    total_votes = sum(state_votes)
    
    # dp[i] 表示获得恰好 i 票的组合数量
    dp = [0] * (total_votes + 1)
    dp[0] = 1  # 0票有1种方式(不选任何州)
    
    # 遍历每个州
    for votes in state_votes:
        # 从后向前更新,避免重复使用同一个州
        for current in range(total_votes, votes - 1, -1):
            dp[current] += dp[current - votes]
    
    # 统计所有 >= target 的组合数量
    return sum(dp[target:])


# 测试
state_votes = [3, 5, 7, 10, 15]
target = 20

result = count_winning_combinations_dp(state_votes, target)
print(f"能赢得选举的组合数量: {result}")