VO #1:
API - storage side
improve latency / performance -> tech stack shift from Java to Rust now
multi-schema for gsi
ddb official docs
BQ1: Unexpected Obstacle -> idempotency (deep dive and communication)
BQ2: anyone reject your idea -> batch edit (accept as constraint for better design + backbone)

VO #2:
Minor follow-ups when introducing 2Wind part
BQ1: complex -> static vs season-varying data separation
why complex
how navigate 
how assumption when separating patterns
how frontend change

BQ2: experience with genAI -> draw the workflow, discuss this "spec-driven testing" method in last 5-min as Amazon is using now

Code: Both need to talk about time and space complexity

here are N products, and we dont know exactly how many categories there are 
and which product belongs to which category. 
We are, however, aware that certain pairs of products belong in the same category.

So, we are given a list of such product ID pairs that identify products belonging to a same category, 
for example: (1, 5), (7, 2), (3, 4), (4, 8), (6, 3), (5, 2)

When we analyze that list, we can see that we only have two categories with 4 products, 
each: (1, 2, 5, 7), (3, 4, 6, 8)

The questions are:

* How many categories we have and How many products in each category?}

# edge case: duplicates; union find
# interviewer's expectation: graph + adj_list
class UnionFind:
    def __init__(self):
        self.root = {}  # id -> root_id
        self.parent = 0
    
    def add(self, n):
        if n in self.root: return
        self.root[n] = n
        self.parent += 1
    
    def find(self, n) -> int:
        # compress path
        if self.root[n] != n:
            self.root[n] = self.find(self.root[n])
        return self.root[n]
    
    def union(self, a, b):
        # fetch both root
        pa, pb = self.find(a), self.find(b)
        if pa == pb: return
        # update one into another
        self.root[pb] = pa
        self.parent -= 1

# Original code
# class Solution:
#     def union(self, ids):
#         #1. init unionfind
#         uf = UnionFind()
#         #2. loop to union
#         for a, b in ids:
#             uf.add(a)
#             uf.add(b)
#             uf.union(a, b)
        
#         def countCategories(self) -> int:
#             return uf.parent
        
#         def countProducts(self) -> List[List[int]]:
#             record = defaultdict(list)
#             for id, root in uf.root.items():
#                 root = uf.find(root)
#                 if root not in record: record[root].append(root)
#                 record[root].append(id)
#             return record.values()
        ---
# Claude Fix
class Solution:
    def __init__(self, ids):
        self.uf = UnionFind()
        for a, b in ids:
            self.uf.add(a)
            self.uf.add(b)
            self.uf.union(a, b)

    def countCategories(self) -> int:
        return self.uf.parent

    def countProducts(self):
        record = defaultdict(list)
        for id in self.uf.root:
            root = self.uf.find(id)
            record[root].append(id)
        return list(record.values())
        
Time Complexity: O(n * α(n)) where α(n) ≤ 4; O(n × size of largest set) if no path compression
Space Complexity: O(n) 
########################################



## Goldbach Conjecture tells for any whole even number greater than 2
## can be represented as a sum of 2 prime numbers.
## For example 
## 18 = 13 + 5   OR 7 + 11
## 8 = 3 + 5
## 4 = 2 + 2
## 10 = 5 + 5    OR 7 + 3
## 12 = 5 + 7
## 14 = 7 + 7    Or 11 + 3
## .....
## More info in this Youtube short: https://www.youtube.com/shorts/2DDobIN5L0M
## Given An integer "a" can you prove/disprove Goldbach Conjecture.
## Print the prime numbers representing "a" if they exists.


def isGoldbachConjectureCorrect(a):
    def prime(x: int) -> bool:
        j = 2
        while j * j <= x:
            if x % j == 0: return False
            j += 1
        return True
# Original - I make the assumption that input is even number > 2, forget to clarify
    # # 1. loop prime number <= a/2
    # for i in range(3, a // 2):
    #     if prime(i) and prime(a - i): return [i, a - i]
    # return [-1, -1]
# Update by Claude for edge cases
    if a <= 2 or a % 2 != 0:
        return [-1, -1]

    for i in range(2, a // 2 + 1):
        if prime(i) and prime(a - i):
            return [i, a - i]
    return [-1, -1]

Time Complexity: O(n · sqrt(n))
Space Complexity: O(1)

1*16
2*8
4*4
8*2
16*1