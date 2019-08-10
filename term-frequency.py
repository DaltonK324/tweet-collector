"""
This program is designed to collect frequent terms of tweet messages.
"""

from collections import Counter
from nltk.corpus import stopwords
import json
import os
import re
import argparse

def get_parser():
    """Get parser for command line arguments."""
    parser = argparse.ArgumentParser(description="Tweet Downloader")
    parser.add_argument(
        "-d",
        "--dir",
        dest="dir",
        help="Directory of input files",
        default=''
    )

    parser.add_argument(
        "-fc",
        "--freqCount",
        dest="fc",
        help="Display top N most frequent words",
        default=10
    )

    parser.add_argument(
        "-sw",
        "--stopwords",
        dest="sw",
        help="Extra stop words",
        default=''
    )
    return parser

def getFreqTerms(path, sw,fc):
    files = os.listdir(path)
    freq = Counter()
    for file in files:
        if file.endswith('json'):
            print("Processing {}. This may take awhile...".format(file))
            with open(path+file) as f:
                tweets = f.readlines()
                for tweet in tweets:
                    tweetObj = json.loads(tweet)
                    freq += Counter(cleanTweet(tweetObj['text'].split(),sw))

    for item in freq.most_common(int(fc)):
        print("{}\t{}".format(item[0].encode('utf-8'), item[1]))

def cleanTweet(dirtyTweet,sw):
    cleanT = [re.sub(r'[^\w\s]', '', word) for word in dirtyTweet]  # Remove Punctuation
    cleanT = [word.lower().strip() for word in cleanT]  # Remove whitespace and lower words
    cleanT = [word for word in cleanT if word not in stopwords.words('english') + sw + [' ', 'use','rt']] # Remove General Stopwords

    return cleanT


@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    print("\nIgnoring words: {}".format(args.sw))
    print("Displaying the top {} most frequent words".format(args.fc))
    print("Pulling files from {}\n".format(os.getcwd() + '\\' + args.dir))

    getFreqTerms('./' + args.dir,args.sw.split(','),args.fc)
