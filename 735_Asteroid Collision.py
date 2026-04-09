class Solution:
    def asteroidCollision(self, asteroids: List[int]) -> List[int]:
        # Positive (Right); Negative (Left)
        # Smash Case: cur left while prev right
        q = []

        for a in asteroids:
            if not q or a > 0: q.append(a)
            elif a < 0: 
                # prev as RIGHT
                while q and 0 < q[-1] < -a: q.pop()
                # check residual
                if not q or q[-1] < 0: q.append(a)
                elif q[-1] == -a: q.pop()
        
        return q