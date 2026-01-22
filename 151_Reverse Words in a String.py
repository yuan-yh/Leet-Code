# class Solution:
#     def reverseWords(self, s: str) -> str:
#         s = s.split()
#         s.reverse()
#         return " ".join(s)

class Solution:
    def reverseWords(self, s: str) -> str:
        def reverse(start, end):    # [start, end]
            while start < end:
                chars[start], chars[end] = chars[end], chars[start]
                start += 1
                end -= 1
        
        # For O(1) space complexity if mutable string
        chars = list(s)
        length = len(chars)
        
        # 1. reverse the entire string
        reverse(0, length - 1)
        # 2. mirror each word
        slow = fast = 0
        while fast < length:
            # A. find the word start
            while fast < length and chars[fast] == " ": fast += 1
            if fast == length: break

            # B. fill the space between words
            if slow > 0:
                chars[slow] = " "
                slow += 1
            
            # C. insert till the word end
            start = slow
            while fast < length and chars[fast] != " ": 
                chars[slow] = chars[fast]
                fast += 1
                slow += 1
            
            # D. flip the word
            reverse(start, slow-1)
        
        return "".join(chars[:slow])