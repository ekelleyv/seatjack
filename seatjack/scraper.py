import twitter

from seatjack.config import *
from seatjack.tables import ImageTweet
from seatjack.db import Session

class TwitterScraper(object):
    """docstring for TwitterScraper"""
    def __init__(self):
        super(TwitterScraper, self).__init__()
        self.twitter_client = twitter.Api(consumer_key=TWITTER_API_KEY, consumer_secret=TWITTER_API_SECRET,
            access_token_key=TWITTER_ACCESS_TOKEN, access_token_secret=TWITTER_ACCESS_SECRET)

    def _get_tweets(self, search_term, start_id=None):
        # LOLHACKS
        term_string = "%s" % search_term
        tweets = self.twitter_client.GetSearch(term=term_string, count=100, include_entities=True, result_type="recent", max_id=start_id)
        # print tweets
        return tweets

    def scrape_history(self, start_id=None, target_number=1000):
        image_tweets = []
        min_id=start_id

        while len(image_tweets) < target_number:

            tweets = self._get_tweets("\"got my tickets\" OR \"got my ticket\" OR \"my tickets came\" OR \"my ticket came\" OR \"got tickets\" OR \"got a ticket\" filter:images", start_id=min_id)
            print len(image_tweets), len(tweets), min_id, tweets[0].id

            min_id = tweets[-1].id

            for tweet in tweets:
                # print tweet.created_at
                if tweet.media and tweet.retweeted == False:
                    image_tweets.append(tweet)

        session = Session()

        for tweet in image_tweets:
            print tweet.id, tweet.media[0]["media_url"], tweet.text
            try:
                it = ImageTweet(tweet_id=tweet.id,
                                original_image_url=tweet.media[0]["media_url"].encode('utf-8'),
                                tweet_body=tweet.text.encode('utf-8'))
                session.add(it)
            except:
                print "Can't decode"


        session.commit()

        session.close()



if __name__ == '__main__':
    ts = TwitterScraper()
    ts.scrape_history(start_id=598995076124155905)
