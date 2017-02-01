import nltk
from nltk.corpus import stopwords, opinion_lexicon
from collections import Counter, defaultdict
import json
import re
import string
import math

#### setup tweet parsing ####

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

def tweets_list():
    with open('tweets.txt', 'r') as file:
        return [json.loads(line) for line in file if "#trndnl" not in line]


punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via', '…', '⒌','⒋', '⒊', '⒉', '⒈', 'inauguration', '#inauguration']


#### 

def common_word_counter(tweets):
    counter = Counter()
    for tweet in tweets:
        terms = [term for term in preprocess(tweet['text'], lowercase=True)
                 if term not in stop 
                 and not term.startswith(('#', '@'))]
        counter.update(terms)
    return counter

def common_words(length):
    counter = common_word_counter()
    return counter.most_common(length)

# co-occurence matrix

def cooccurence_matrix(tweets):
    com = defaultdict(lambda : defaultdict(int))
    for tweet in tweets:
        terms_only = [term for term in preprocess(tweet['text'], lowercase=True)
                      if term not in stop
                      and not term.startswith(('@'))]
        for i in range(len(terms_only)-1):            
            for j in range(i+1, len(terms_only)):
                w1, w2 = sorted([terms_only[i], terms_only[j]])                
                if w1 != w2:
                    com[w1][w2] += 1
    return com


def probabilities(word_occurences, word_coocurences, sample_size):
    probability_word = {}
    probability_cooccurence = defaultdict(lambda : defaultdict(int))
    for term, n in word_occurences.items():
        probability_word[term] = n / sample_size
        for term2 in word_coocurences[term]:
            probability_cooccurence[term][term2] = word_coocurences[term][term2] / sample_size
    return probability_word, probability_cooccurence


def calculate_semantic_orientations(probability_word, probability_cooccurences, positive_words, negative_words):
    pmi = defaultdict(lambda : defaultdict(int))
    for term1 in probability_word:
        for term2 in probability_cooccurences[term1]:
            numerator = probability_cooccurences[term1][term2]
            if numerator != 0:
                try:
                    pmi[term1][term2] = math.log2(numerator) / (probability_word[term1] * probability_word[term2])
                except KeyError as e:
                    print(term1," ", term2)


    semantic_orientation = {}
    count = len(probability_word)
    for term, _ in probability_word.items():
        positiveness = sum(pmi[term][known_word] for known_word in positive_words)
        negativeness = sum(pmi[term][known_word] for known_word in negative_words)
        semantic_orientation[term] = positiveness - negativeness
        count = count - 1
        print(count)
    return semantic_orientation

def score_tweets(tweets, semantic_orientations):
    processed_tweets = []
    for tweet in tweets:
        acc = 0
        for word in tweet['text']:
            try:
                acc += semantic_orientations[word]
            except KeyError:
                pass
        tweet_map = {'text' : tweet['text'],
                     'coordinates' : tweet['coordinates']['coordinates'],
                     'score' : acc / len(tweet['text'])}
        processed_tweets.append(tweet_map)
    return processed_tweets

def write_tweets(tweets):
    with open('scored_tweets.txt','w+') as file:
        for tweet in tweets:
            json.dump(tweet, file)
            file.write('\n')
    
def _main_():
    tweets = tweets_list()
    size = len(tweets)
    word_occurences = common_word_counter(tweets)
    word_cooccurences = cooccurence_matrix(tweets)
    probability_word, probability_cooccurence = probabilities(word_occurences, word_cooccurences, size)
    positive_words = nltk.corpus.opinion_lexicon.positive()
    negative_words = nltk.corpus.opinion_lexicon.negative()
    semantic_orientations =  calculate_semantic_orientations(probability_word, probability_cooccurence, positive_words, negative_words)
    scored_tweets = score_tweets(tweets, semantic_orientations)
    write_tweets(scored_tweets)
    
