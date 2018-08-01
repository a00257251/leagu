import unittest
from Tweeter import selectTweets,tweetSearch


class Tweeter(unittest.TestCase):

    def setUp(self):
        pass

    def test_selectTweets(self):
        self.assertEqual(selectTweets('22'),[{'username': u'22', 'url': u'22', 'tweet': u'22', 'TweetTime': u'22', 'userPhoto': u'22'}])


if __name__ == '__main__':
    unittest.main()