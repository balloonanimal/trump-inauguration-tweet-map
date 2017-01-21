from TwitterSearch import *

try:
    tso = TwitterSearchOrder()  # create a TwitterSearchOrder object
    tso.set_keywords(['#inauguration'])  # let's define all words we would like to have a look for
    tso.set_language('en')
    tso.set_include_entities(False) # and don't give us all those entity information

    # it's about time to create a TwitterSearch object with our secret tokens
    ts = TwitterSearch(
        consumer_key = 'NdjZ21poYPH5CsYWRDrqOm6oZ',
        consumer_secret = '2FWSpdL7vIwGDmNrEkmLNRGv4GTuoiYTOTKVyHzKuVz1WGOuWY',
        access_token = '822627811227738117-7vzke77zdqaecczB4TdSon7V1smppNf',
        access_token_secret = 'Q3S92qdAEiFewtHbT4vL75VJ3G6p0yPKCQHP4yBAt6eUM'
     )

    client = MongoClient()
    db = client['twitter_db']
    collection = db['twitter_collection']

     # this is where the fun actually starts :)
#     for tweet in ts.search_tweets_iterable(tso):
         

except TwitterSearchException as e: # take care of all those ugly errors if there are some
    print(e)
