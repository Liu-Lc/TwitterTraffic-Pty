class Tweet():
    def __init__(self, tweetid, userid, username, text, date, link):
        self.tweetid = tweetid
        self.userid = userid
        self.username = username
        self.text = text
        self.date = date
        self.link = link

# class incident to add to DB
class Incident:
    def __init__(self, tweetid, place, isAccident, isObstacle, isDanger):
        self.tweetid = tweetid
        self.place = place
        self.isAccident = isAccident
        self.isObstacle = isObstacle
        self.isDanger = isDanger