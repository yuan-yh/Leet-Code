class Solution:
    def closestMeetingNode(self, edges: List[int], node1: int, node2: int) -> int:
        # Find the node that is reachable by both node1 and node2, w/ min distance from them (get the min idx one when same distance)
        l = len(edges)

        def calc_dis(start: int) -> List[int]:
            dis = [l] * l
            cur = 0
            # terminate when out of scope or visited
            while start >= 0 and dis[start] == l:
                dis[start] = cur
                cur += 1
                start = edges[start]
            return dis
        
        dis1 = calc_dis(node1)
        dis2 = calc_dis(node2)

        minD, minIdx = l, -1

        for i, (d1, d2) in enumerate(zip(dis1, dis2)):
            curD = max(d1, d2)
            if curD < minD: minD, minIdx = curD, i
        return minIdx