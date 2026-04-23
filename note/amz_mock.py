Daniel Yu: internal test framework
sqa
AI
voice call (aspect related to audio)
alexa audio feature

----
You are given a 2D grid representing a terrain map with three types of cells:

'T' - Radio tower (emits signals)
'M' - Mountain (blocks signals)
'.' - Empty cell (signals pass through)
Each radio tower broadcasts signals in 4 cardinal directions (up, down, left, right). A signal travels in a straight line until it either:

Hits a mountain (signal stops)
Reaches the grid boundary (signal stops)
Your task: Determine which pairs of radio towers can communicate with each other. Two towers can communicate if a signal from one tower can reach the other tower.


grid = [
    ['T', '.', '.', 'T'],
    ['.', 'M', '.', '.'],
    ['T', '.', '.', 'T']
]


grid = [
    ['.', 'T', '.', 'T'],
    ['.', 'M', '.', '.'],
    ['T', '.', '.', 'T']
]



Example 1: Basic Line of Sight
Input:

T . . T
. . . .
T . . T

Signal Propagation:

Tower (0,0) → → → reaches Tower (0,3) ✓
Tower (0,3) ↓ ↓ reaches Tower (2,3) ✓
Tower (2,0) → → → reaches Tower (2,3) ✓
Tower (0,0) → → → reaches Tower (2,0) 

Output:

[
    ((0, 0), (0, 3)),  # Top-left ↔ Top-right
    ((0, 3), (2, 3)),  # Top-right ↔ Bottom-right
    ((2, 0), (2, 3))   # Bottom-left ↔ Bottom-right
]

Total communicating pairs: 3

Example 2: Mountain Blocking
Input:

T . M . T
. . . . .
T . . . T

Signal Propagation:

Tower (0,0) → → X (blocked by mountain at (0,2))
Tower (0,4) ↓ ↓ reaches Tower (2,4) ✓
Tower (2,0) → → → → reaches Tower (2,4) ✓

Output:

[
    ((0, 4), (2, 4)),  # Top-right ↔ Bottom-right
    ((2, 0), (2, 4))   # Bottom-left ↔ Bottom-right
]

Total communicating pairs: 2
Note: Tower (0,0) is isolated - mountain blocks its signal to (0,4)

Example 3: No Communication
Input:

T M T
M . M
T M T

Signal Propagation:

All towers are surrounded by mountains - no signals can reach other towers

Output:

[]

Total communicating pairs: 0

# Clarify: O(N)
# Clarify: 只配对相邻的塔 OR 收集所有两两配对

# Tip: 写完主逻辑后，主动列出 3-5 个 edge case 并口头或手动验证。
# Tip: 面试中要边想边说，解释你为什么选这个数据结构、为什么这样遍历、时间复杂度是多少。
# Tip: 写完代码后，用一个小例子dry run，跟面试官说"让我 trace 一下确认正确性"。
class Solution:
    def countPair(self, grid: List[List[char]]):
        row, col = len(grid), len(grid[0])
        res = []
        # 1. detech Towers connected in the same row
        for r in range(row):
            prevc = None
            for c in range(col):
                # case: '.', 'T', 'M'
                if grid[r][c] == 'M': prevc = None
                elif grid[r][c] == 'T': 
                    if prevc is not None: res.append(((r, prevc), (r, c)))
                    prevc = c
        
        # 2. detech Towers connected in the same column
        for c in range(col):
            prevr = None
            for r in range(row):
                # case: '.', 'T', 'M'
                if grid[r][c] == 'M': prevr = None
                elif grid[r][c] == 'T': 
                    if prevr is not None: res.append(((prevr, c), (r, c)))
                    prevr = r
        
        return res
