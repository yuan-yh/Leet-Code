def ip_to_int(ip):
    """将IP转换为整数便于比较"""
    parts = list(map(int, ip.split('.')))
    return (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3]

def find_city(ip, ranges):
    """
    找到IP对应的城市
    
    参数:
        ip: 查询的IP地址，如 "1.2.3.50"
        ranges: IP区间列表，如 [("1.2.3.1", "1.2.3.100", "New York"), ...]
    
    返回:
        城市名称或None
    """
    ip_num = ip_to_int(ip)
    
    # 将ranges转换为整数并排序
    converted = [(ip_to_int(s), ip_to_int(e), city) for s, e, city in ranges]
    converted.sort()
    
    # 二分查找
    left, right = 0, len(converted) - 1
    
    while left <= right:
        mid = (left + right) // 2
        start, end, city = converted[mid]
        
        if ip_num < start:
            right = mid - 1
        elif ip_num > end:
            left = mid + 1
        else:
            return city
    
    return None

# 测试
ranges = [
    ("1.2.3.1", "1.2.3.100", "New York"),
    ("1.2.3.101", "1.2.3.200", "Boston"),
    ("10.0.0.1", "10.0.0.255", "Chicago")
]

print(find_city("1.2.3.50", ranges))    # New York
print(find_city("1.2.3.150", ranges))   # Boston
print(find_city("10.0.0.100", ranges))  # Chicago
print(find_city("8.8.8.8", ranges))     # None