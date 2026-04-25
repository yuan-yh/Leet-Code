class WordDistance:
    # Track all indexes of words present
    def __init__(self, wordsDict: List[str]):
        self.record = defaultdict(list)
        for i, w in enumerate(wordsDict):
            self.record[w].append(i)

    def shortest(self, word1: str, word2: str) -> int:
        # For 2 sorted arrays, find the pair of elements with the smallest absolute difference
        n1, n2 = self.record[word1], self.record[word2]
        i, j, l1, l2, res = 0, 0, len(n1), len(n2), inf

        while i < l1 and j < l2:
            res = min(res, abs(n1[i] - n2[j]))
            if n1[i] < n2[j]: i += 1
            else: j += 1
        return res


# Your WordDistance object will be instantiated and called as such:
# obj = WordDistance(wordsDict)
# param_1 = obj.shortest(word1,word2)