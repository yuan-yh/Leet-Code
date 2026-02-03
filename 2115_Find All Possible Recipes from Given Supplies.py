class Solution:
    def findAllRecipes(self, recipes: List[str], ingredients: List[List[str]], supplies: List[str]) -> List[str]:
        # Topological Sort: map ingredients -> recipe, then process those w/n in-degrees
        graph = defaultdict(list)
        inDegree = {}
        # 1. map
        for r, ins in zip(recipes, ingredients):
            for i in ins:
                graph[i].append(r)
            inDegree[r] = len(ins)
        # 2. init a queue w/n in-degrees (ingredients)
        q = deque(supplies)
        # 3. process: in-degree - 1 -> record & push into q when in-degree = 0
        res = []

        while q:
            cur = q.popleft()
            for r in graph[cur]:
                inDegree[r] -= 1
                if inDegree[r] == 0:
                    q.append(r)
                    res.append(r)
        
        return res