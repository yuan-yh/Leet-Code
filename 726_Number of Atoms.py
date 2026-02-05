class Solution:
    def countOfAtoms(self, formula: str) -> str:
        # Stack: letter, digit, ()
        stack = [Counter()]
        i, n = 0 , len(formula)

        while i < n:
            cur = formula[i]

            # case: ( - append Counter()
            if cur == "(":
                stack.append(Counter())
                i += 1
            # case: ) - multiply the cur Counter() by the following digit
            elif cur == ")":
                i += 1
                tmpi = i
                while tmpi < n and formula[tmpi].isdigit(): tmpi += 1
                cnt = int(formula[i:tmpi]) if tmpi > i else 1
                i = tmpi

                # process all current Counter * cnt
                tmpc = stack.pop()
                for te, tc in tmpc.items():
                    stack[-1][te] += cnt * tc
            else:
                # case: symbol - loop to complete element name (only the first is the uppercase)
                tmpi = i + 1
                while tmpi < n and formula[tmpi].islower(): tmpi += 1
                element = formula[i : tmpi]
                i = tmpi
                # case: digit - loop to complete digits
                while tmpi < n and formula[tmpi].isdigit(): tmpi += 1
                cnt = int(formula[i : tmpi]) if tmpi > i else 1
                stack[-1][element] += cnt
                i = tmpi

        # Output in lexico order
        res = ""
        for e in sorted(stack[0].keys()):
            res += e
            if stack[0][e] > 1: res += str(stack[0][e])
        return res