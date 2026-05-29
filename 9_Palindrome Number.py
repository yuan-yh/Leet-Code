class Solution:
    def isPalindrome(self, x: int) -> bool:
        # edge case: 10x or negative
        if x < 0 or (x > 0 and x % 10 == 0): return False
        # reverse then compare
        copy, reverse = x, 0
        while copy > 0:
            reverse = reverse * 10 + copy % 10
            copy //= 10
        return reverse == x