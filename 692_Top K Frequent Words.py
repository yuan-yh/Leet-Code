class Word:
    __slots__ = 'word', 'cnt'
    
    def __init__(self, word, cnt):
        self.word = word
        self.cnt = cnt
    
    def __lt__(self, other):
        # case: smaller cnt OR larger lexi order
        if self.cnt != other.cnt: return self.cnt < other.cnt
        return self.word > other.word
    
class Solution:
    def topKFrequent(self, words: List[str], k: int) -> List[str]:
        # Key Insight: min-heap to maintain k max_cnt low_lexi words
        # 堆不是有序数组！
        # 1. count word frequency
        wcnt = Counter(words)
        # 2. loop into the min-heap
        heap = []
        for word, cnt in wcnt.items():
            heappush(heap, Word(word, cnt))
            if len(heap) > k: heappop(heap)
        # 3. reverse min-heap to max-heap
        # !!!堆不是有序数组！
        # heap.reverse()  → 只是把数组元素顺序颠倒
        # heap.sort()     → 真正按比较器排序
        heap.sort(reverse=True)
        # 4. return min-heap items
        return [w.word for w in heap]