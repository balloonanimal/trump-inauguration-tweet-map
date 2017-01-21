import tweepy
import sys
import json

def cache_tweets():    

    query = "inauguration"
    max_tweets = 100000000
    tweets_per_query = 100  # this is the max the API permits
    file_name = 'tweets.txt' 

    auth = tweepy.AppAuthHandler('NdjZ21poYPH5CsYWRDrqOm6oZ', '2FWSpdL7vIwGDmNrEkmLNRGv4GTuoiYTOTKVyHzKuVz1WGOuWY')

    api = tweepy.API(auth, wait_on_rate_limit=True,
				   wait_on_rate_limit_notify=True)

    if (not api):
        print("can't get api")
        sys.exit(1)
        

    since_id = None
    max_id = -1
    count = 0
    with open(file_name, 'w+') as f:
        while count < max_tweets: 
            try:
                if (max_id <= 0):
                    if (not since_id):
                        new_tweets = api.search(q=query, count=tweets_per_query)
                    else:
                        new_tweets = api.search(q=query, count=tweets_per_query,
                                                since_id=sinceId)
                else:
                    if (not since_id):
                        new_tweets = api.search(q=query, count=tweets_per_query,
                                                max_id=str(max_id - 1))
                    else:
                        new_tweets = api.search(q=query, count=tweets_per_query,
                                                max_id=str(max_id - 1),
                                                since_id=since_id)

                if not new_tweets:
                    print("out of tweets")
                    break

                for tweet in new_tweets:
                    if tweet.coordinates is not None:
                        print("found one!")
                        tweet_map = {'text': tweet.text,
                                     'coordinates': tweet.coordinates}
                        json.dump(tweet_map, f)
                        f.write("\n")
                    
                count += tweets_per_query
                print("{0} tweets downloaded".format(count))
                max_id = new_tweets[-1].id


            except tweepy.TweepError as e:
                print('error ', e)

def get_tweet_list():

    file = open('tweets.txt', 'r')
    return [json.load(line) for line in file]


cache_tweets()

