from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
from textblob import TextBlob
import matplotlib.pyplot as plt

#Variables that contains the user credentials to access Twitter API
consumer_key = '3YrUYM1plcPHwIPUMgQX1P84k'
consumer_secret = 'NLd2hDR6LKu3eyeJqaOz2B1EiNCrjmUzdJZGFgA5TfxABpEhMC'
access_token = '925424693678522368-PQMRJCqctZeA1TOKlaIvoMfohg480tb'
access_token_secret = 'YJ89vSJ1RtaXPBqOOgXNrWRw3vJYrw3aShcGSIGbXmOlF'
pos=0
neg=0
neu=0
count=0
geo_count=0
total_count=0
default_data = dict()
maximum=''
#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        global pos
        global neu
        global neg
        global count
        global total_count
        global geo_count
        global maximum
        foo=False

        tweet = json.loads(data) # load tweet content
        #if tweet['coordinates'] != None:
        #     print(tweet['coordinates']['coordinates'], tweet['text'])
        #    print(data)


        if not tweet['text'].startswith('RT'):
            print(tweet['text'])
            if tweet['place']!= None:
                geo_count +=1
                for i in default_data.items():
                    if tweet['place']['country_code'] in default_data:
                        foo=True
                    else:
                        foo=False
                if foo==True:
                    default_data[tweet['place']['country_code']] += 1
                else:
                    default_data[tweet['place']['country_code']] = 1
                maximum = max(default_data, key=default_data.get)  # Just use 'min' instead of 'max' for minimum.
                print('hey!GeoLocationEnabled')
                print(maximum, default_data[maximum])

            count+=1
            total_count+=1
            analysis = TextBlob(tweet['text'])
            polar = analysis.sentiment.polarity
            if polar >0:
                print('positive')
                pos+=1

            elif polar==0:
                print('neutral')
                neu+=1

            else:
                print('negative')
                neg+=1

        if count==5:
            plt.clf()
            labels = 'Positive', 'Neutral', 'Negative'
            sizes = [pos, neu, neg]
            colors = ['yellowgreen', 'gold', 'lightcoral']
            plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
            plt.axis('equal')
            #plt.title("negative="+str(neg),loc='left')
            if bool(default_data) == False:
                plt.title("whynogeo")
            else:
                plt.title('most location enabled users are from \n'+maximum+','+str(default_data[maximum])+'/'+str(geo_count))
            plt.title("total_count="+str(total_count),loc='right')
            plt.ion()
            plt.show()
            plt.pause(0.05)
            count=0






        # print(data)
        return(True)


    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=["bitcoin"])
