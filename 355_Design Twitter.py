class Twitter:
    def __init__(self):
        # Tweets pool: key - uId, val - [(uId, tid, timestamp)]
        # Follow pool: key - uId, val - set(uId)
        self.tweets = defaultdict(list)
        self.follows = defaultdict(set)
        self.timestamp = 0

    def postTweet(self, userId: int, tweetId: int) -> None:
        # append (uid, tid, timestamp), then update timestamp
        self.tweets[userId].append((userId, tweetId, -self.timestamp))
        self.timestamp += 1

    def getNewsFeed(self, userId: int) -> List[int]:
        # build max-heap for the latest tweets
        heap = []

        # 1. fetch the last tweet from self & followees
        if self.tweets[userId]:
            lastu, lastt, lasttime = self.tweets[userId][-1]
            # time, uid, tid, index
            heappush(heap, (lasttime, lastu, lastt, len(self.tweets[userId]) - 1))
        
        followee = self.follows[userId]
        for f in followee:
            if self.tweets[f]:
                lastu, lastt, lasttime = self.tweets[f][-1]
                # time, uid, tid, index
                heappush(heap, (lasttime, lastu, lastt, len(self.tweets[f]) - 1))
        
        res = []
        # 2. loop heap: terminate when empty || res == 10
        while heap and len(res) < 10:
            # 3. fetch the cur tweet -> push if has more recent tweet
            curtime, curu, curt, curidx = heappop(heap)
            res.append(curt)
            if curidx > 0:
                # uid, tid, timestamp
                nextu, nextt, nexttime = self.tweets[curu][curidx - 1]
                # time, uid, tid, index
                heappush(heap, (nexttime, nextu, nextt, curidx - 1))
        return res

    def follow(self, followerId: int, followeeId: int) -> None:
        self.follows[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        if followeeId in self.follows[followerId]: self.follows[followerId].remove(followeeId)
        


# Your Twitter object will be instantiated and called as such:
# obj = Twitter()
# obj.postTweet(userId,tweetId)
# param_2 = obj.getNewsFeed(userId)
# obj.follow(followerId,followeeId)
# obj.unfollow(followerId,followeeId)