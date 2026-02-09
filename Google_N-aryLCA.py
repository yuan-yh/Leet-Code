def lowestCommonAncestor(root, p, q):
    if not root or root == p or root == q:
        return root
    
    # 区别就在这里：遍历所有children而不是只看left/right
    found = []
    for child in root.children:
        result = lowestCommonAncestor(child, p, q)
        if result:
            found.append(result)
    
    # 如果在两个不同的子树中分别找到了p和q
    if len(found) == 2:
        return root
    # 如果只在一个子树中找到
    if len(found) == 1:
        return found[0]
    return None