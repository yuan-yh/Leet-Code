def decompress(s: str) -> str:
    stack = []
    current = ""
    i = 0
    
    while i < len(s):
        char = s[i]
        
        if char == '(':
            # 把当前结果压栈，开始新的一层
            stack.append(current)
            current = ""
            i += 1
            
        elif char == ')':
            # 这一层结束，下一个一定是 {数字}
            i += 1  # 跳过 )
            i += 1  # 跳过 {
            
            # 读取数字（可能是2位数，如 12, 99）
            num_str = ""
            while s[i] != '}':
                num_str += s[i]
                i += 1
            i += 1  # 跳过 }
            
            repeat_times = int(num_str)
            
            # 弹出栈顶，合并结果
            prev = stack.pop()
            current = prev + current * repeat_times
            
        else:
            # 普通字符，直接加到当前字符串
            current += char
            i += 1
    
    return current