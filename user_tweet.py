#!/usr/bin/env python
# encoding: utf-8

import tweepy  # https://github.com/tweepy/tweepy
import csv
import argparse
import os
from tweepy import AppAuthHandler
import config
import json
import datetime
import sys

# Twitter API credentials
consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_key = config.access_token
access_secret = config.access_secret

def get_parser():
    """Get parser for command line arguments."""
    parser = argparse.ArgumentParser(description="Tweet Downloader")
    parser.add_argument("-s",
                        "--screenname",
                        dest="screenName",
                        help="Username(s) of a twitter account",
                        default=None)
    parser.add_argument("-f",
                        "--fromDate",
                        dest="start",
                        help="Specifies only tweets after selected date",
                        default=None)
    parser.add_argument("-u",
                        "--untilDate",
                        dest="end",
                        help="Specifies only tweets before selected date",
                        default=None)

    return parser

def write_tweets_to_file(screen_name, tweets):
    # write the csv
    with open('%s_tweets.json' % screen_name, 'wb') as f:
        for tweet in tweets:
            f.write(json.dumps(tweet._json)+"\n")
    pass

def time_check(alltweets, new_tweets, start, end, fTweet):
    newT = False
    inRangeTweets = []
    for tweet in new_tweets:
        inRangeS = False
        inRangeE = False
        if start != None:
            if (start-tweet.created_at).days < 0: # If tweet was created on or after the start date, True
                inRangeS = True
        else:
            inRangeS = True

        if end != None:
            if (tweet.created_at-end).days < 1: # If tweet was created on or before the end date, True
                inRangeE = True
        else:
            inRangeE = True

        if inRangeE==True:
            if inRangeS==True: # If tweet is within the given range, save for output
                newT=True # Indicates that a tweet in the date range was found in the batch of tweets
                fTweet=True # Indicates that a tweet in the date range was found
                inRangeTweets.append(tweet)
    alltweets.extend(inRangeTweets)
    return newT, fTweet

def endCheck(newTweetFound, anyTweetFound):
    if newTweetFound==False:
            if anyTweetFound==True: # If tweets were found in the date range, and you didn't find any new tweets to add in the last group of tweets, then there are no more tweets in the date range to grab
                return True
    return False

def get_all_tweets(screen_name, api, start, end):
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    anyTweetFound = False
    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    newTweetFound, anyTweetFound = time_check(alltweets, new_tweets, start, end, anyTweetFound)

    # save the id of the oldest tweet less one
    if alltweets != []:
        oldest = alltweets[-1].id - 1
    else:
        oldest = new_tweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        if endCheck(newTweetFound, anyTweetFound):
            break
        print "getting tweets before '%s'" % (oldest)

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest, since_id=start)
        #write_tweets_to_file(screen_name, new_tweets)
        # # save most recent tweets
        newTweetFound, anyTweetFound = time_check(alltweets, new_tweets, start, end, anyTweetFound)
        if endCheck(newTweetFound, anyTweetFound):
            break

        # update the id of the oldest tweet less one
        if alltweets != []:
            oldest = alltweets[-1].id - 1
        else:
            oldest = new_tweets[-1].id - 1

        print "...%s tweets downloaded so far" % (len(alltweets))

    # transform the tweepy tweets into a 2D array that will populate the csv
    #outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
    write_tweets_to_file(screen_name, alltweets)

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    if args.start != None:
        try:
            sDate = datetime.datetime.strptime(args.start, '%d%b%Y')
        except ValueError:
            print("Error: Incorrect Date format: fromDate. Please input a valid date in the format: DDMMYYY")
            sys.exit(1)
    else:
        sDate = None

    if args.end != None:
        try:
            eDate = datetime.datetime.strptime(args.end, '%d%b%Y')
        except ValueError:
            print("Error: Incorrect Date format: untilDate. Please input a valid date in the format: DDMMYYY")
            sys.exit(1)
    else:
        eDate = None
        
    if sDate != None:
        if eDate != None:
            if (sDate-eDate).days > 0:
                print("Error: Incorrect Date range. Please write the earliest date you wish to collect tweets in the '--fromDate' field, and the latest date you wish to collect tweets from in the '--untilDate' field.")
                sys.exit(1)

    if args.screenName==None:
        print("Error: No screenname provided. Please include a screenname to pull tweets from (Usage is as follows: --screenname=user1,user2). See README.md for more info.")
    else:
        screenNameList = args.screenName.split(",")
        
        auth = AppAuthHandler(config.consumer_key, config.consumer_secret)
        # auth.set_access_token(config.access_token, config.access_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        # pass in the username of the account you want to download
        for name in screenNameList:
            print "Screen Name: {}".format(name)
            get_all_tweets(name, api, sDate, eDate)
            print