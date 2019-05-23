import sys,tweepy,csv,re
from tkinter import *

from tweepy import TweepError

import twitter_credentials as tc

class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = tweepy.API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in tweepy.Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in tweepy.Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in tweepy.Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets


class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = tweepy.OAuthHandler(tc.CONSUMER_KEY, tc.CONSUMER_SECRET)
        auth.set_access_token(tc.ACCESS_TOKEN, tc.ACCESS_TOKEN_SECRET)
        return auth


class TwitterAPI:

    def __init__(self):
        self.tweetText = []
        self.tweetLikes = []
        self.tweetRetweet = []
        self.tweetDates = []

    def DownloadData(self,tweets):
        # Open/create a file to append data to
        csvFile = open('result.txt', 'w+')
        # iterating through tweets fetched
        for tweet in tweets:
            #Append to temp so that we can store in csv later. I use encode UTF-8
            self.tweetText.append(tweet.text.encode('utf-8'))
            self.tweetLikes.append(tweet.favorite_count)
            self.tweetRetweet.append(tweet.retweet_count)
            self.tweetDates.append(tweet.created_at)

        for count in range(len(self.tweetText)):
            self.info = str(self.tweetText[count])
            self.likes = str(self.tweetLikes[count])
            self.retweets = str(self.tweetRetweet[count])
            self.dates = str(self.tweetDates[count])

            #Write to csv and close csv file
            csvFile.write("\nDate: ")
            csvFile.write(self.dates.replace('b', '', 1))
            csvFile.write("\n")
            csvFile.write(self.info.replace('b','',1))
            csvFile.write("\nLikes: ")
            csvFile.write(self.likes.replace('b','',1))
            csvFile.write("\tRetweets: ")
            csvFile.write(self.retweets.replace('b', '', 1))
            csvFile.write("\n")
        csvFile.close()

def search(event):
    user = username.get()
    count = int(num.get())
    try:
        twitter_client = TwitterClient()
        api = twitter_client.get_twitter_client_api()
        tweets = api.user_timeline(screen_name=user, count=count)
        sa = TwitterAPI()
        sa.DownloadData(tweets)

        window.destroy()

        f1 = open("result.txt",'r')
        data = f1.read()

        #Creating root newwindow
        newwindow = Tk()
        newwindow.title("TWITTER")
        newwindow.geometry('920x720')
        newwindow.configure(background='#00acee')

        # User Details
        print_tweets = Label(newwindow, text=count, justify=CENTER, background='#00acee', fg='#ffffff')
        print_tweets.place(x=10, y=10)
        print_tweets = Label(newwindow, text="tweets of", justify=CENTER, background='#00acee', fg='#ffffff')
        print_tweets.place(x=35, y=10)
        print_tweets = Label(newwindow, text=user, justify=CENTER, background='#00acee', fg='#ffffff')
        print_tweets.place(x=90, y=10)

        # Printing Tweets
        print_tweets = Label(newwindow, text=data, justify=LEFT, background='#00acee')
        print_tweets.place(x=10, y=30)

        exit_button = Button(newwindow, bg='#ffffff', text="Exit", fg='#00acee', width=15)
        exit_button.bind("<Button-1>", exit)
        exit_button.place(x=950, y=600)

        newwindow.mainloop()
        f1.close()

    except tweepy.error.TweepError:
        error = Label(window, text="Username Invalid.")
        error.place(x=10,y=70)


#Creating root window
window = Tk()
window.title("TWITTER")
window.geometry('920x720')
window.configure(background='#00acee')

#Twitter logo in background
gui_logo = PhotoImage(file='final.png')
gui_logo_label = Label(window, image=gui_logo, background='#00acee')
gui_logo_label.pack()

#Search_text of twitter username and number of tweets
twitter_user = Label(window, text="Enter Twitter username: ")
twitter_user.config(bg='#00acee', fg='#ffffff')
twitter_user.place(x = 10, y = 10)

username = Entry(window)
username.place(x=200,y = 10)

num_tweets = Label(window,text="Number of Tweets: ")
num_tweets.config(bg='#00acee', fg='#ffffff')
num_tweets.place(x=10, y=40)

num = Entry(window)
num.place(x=200, y=40)

#Search Button
search_user = Button(window, bg='#ffffff', text="Search user", fg='#00acee', width=15)
search_user.bind("<Button-1>",search)
search_user.place(x=400,y=10)

window.mainloop()