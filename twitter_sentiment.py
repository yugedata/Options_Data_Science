from nltk.sentiment.vader import SentimentIntensityAnalyzer
import tweepy
import csv
import pandas
import time

twitter_keys = tweepy.OAuthHandler('FEDY2PLyk64g7m7VddeF8FTd9', 'GGJlukrQHT1XV9BzWInL6vgVOq0Xy7T93YVoG4paSOZ6ayftKp')

twitter_keys.set_access_token('973948809704366083-3nswKEYaZYllzJFkikfs6iVtyIZCBBN',
                              'Tlj2GdnSRQ7t4q1lMyyv3llPgs21b5bol48prqrpQcAff')

access = tweepy.API(twitter_keys, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# write tweets to a csv file
fileOpens = open("test.csv", 'a')
fileWrite = csv.writer(fileOpens)

arrTweets = []
numTweets = 0
geoCode = "40.726673,-74.067391,30km"  # geo code of dt Manhattan
repeated = 0

for tweet in tweepy.Cursor(access.search, q='covid19',
                           count=10,
                           lang="en", since="2020-04-09",
                           ).items():
    # for x in arrTweets:
    #    if str(tweet) == str(x):
    #        repeated += 1

    arrTweets.append(str(tweet))
    numTweets += 1
    # print(numTweets)
    print(tweet.created_at, tweet.text)
    print()
    fileWrite.writerow([tweet.created_at, tweet.text.encode('utf-8')])

print(len(arrTweets))

sia = SentimentIntensityAnalyzer()
num = 0

for t in arrTweets:
    print(t)
    siaTweet = sia.polarity_scores(t)
    num += 1
    for n in sorted(siaTweet):
        print('{0}: {1}, '.format(n, siaTweet[n]), end='')
        print()
        # fileWrite.writerow('{0}: {1}, '.format(n, siaTweet[n]), end='')

fileOpens.close()
print(repeated)
print(numTweets)
print(num)
