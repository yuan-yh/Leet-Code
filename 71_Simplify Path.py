class Solution:
    def simplifyPath(self, path: str) -> str:
        # Key Insight: split by '/' -> stack -> pop if .. -> output
        # 1. split by '/'
        parray = path.split('/')
        # 2. loop and stack
        stack = []
        for add in parray:
            # case: ./../empty/others
            if len(add) == 0 or add == '.': continue
            elif add == '..': 
                if len(stack) > 0: stack.pop()
            else: stack.append(add)

        # 3. pop to output
        return '/' + '/'.join(stack)

"""
1) . = cur
2) ..  = prev
3) // or /// = /
4) .>2 like ... or .... = dir or file name
split into a stack then array

Output:
1. start /
2. split by / ---> '/'.join()
3. only root ends with /
4. no single or double .
"""