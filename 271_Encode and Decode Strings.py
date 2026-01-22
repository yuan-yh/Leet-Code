class Codec:
    def encode(self, strs: List[str]) -> str:
        """Encodes a list of strings to a single string.
        """
        res = ""
        for s in strs:
            res += str(len(s)) + '#' + s
        return res
        

    def decode(self, s: str) -> List[str]:
        """Decodes a single string to a list of strings.
        """
        p = 0
        res = []

        while p < len(s):
            length = 0
            # 1. count word length
            while p < len(s) and s[p] != '#':
                length = length * 10 + int(s[p])
                p += 1
            # 2. skip '#'
            p += 1
            # 3. append s[p : p + length]
            res.append(s[p : p + length])
            p += length
        return res
        


# Your Codec object will be instantiated and called as such:
# codec = Codec()
# codec.decode(codec.encode(strs))