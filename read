## Command line tool to collect tweets data by keywords and date range - run.py

1. Make sure you have python installed and import tweepy package.

    Follow this link to learn about TweePy package

    https://github.com/tweepy/tweepy

1. Rename file config.py.dist to config.py

1. Edit config.py with your app authentication tokens

1. Enjoy the command line

### Usage
```
python run.py --startDate=YYYY-MM-DD --endDate=YYYY-MM-DD --keyword=your-key-word
```

### Sample Result
We download tweets related to Harvey storm available at this link:

https://drive.google.com/drive/folders/0Bz0t5Fi0GA75bzNpWVhaSElOOVU

## Command line tool to calculate term frequency from the twitter data - term-frequency.py

* **term-frequency.py** calculator looks for *.json* files that are output by **run.py**
* This program only outputs command line information, so take note of the console output

### Commands

* **Directory:** `-d | --dir` will allow the program to know where the *.json* files are located. Folder/Files must be in the tweet-collector root

* **Stopwords:** `-sw | --stopwords` will block any additional words that you want to remove from the frequency calculator

* **Frequency Count:** `-fc | --freqCount` will set the N number up terms that will be displayed 

```
python term-frequency.py --dir=output/ --stopwords=opioid,rt,day,calm --freqCount=3

addiction       1045
epidemic        987
overdose        665
```

## Command line tool to pull twitter user histories - user_tweet.py
The purpose of this program is to retrieve a twitter user's tweet history, outputting it to a JSON file format. Below are instructions for the use of this program

### Commands
* **Twitter Screenname:** `-s | --screenname` allows the user to input the user(s) to retrieve tweet history(s) from.

* **From Date:** `-f | --fromDate` allows the user to specify that they want to retrieve tweets on and after the selected date. 

* **Until Date:** `-u | --untilDate` allows the user to specify that they want to retrieve tweets on and before the selected date.  

### Execution
```
python user_tweet.py --screenname=user1,user2,user3 --fromDate=02Feb2018 --untilDate=04Feb2018
```
One or more screennames are required to run the above line of code (if inputting more than 1 screenname, seperate each screenname with a single comma). Dates must be given in the format: **DDMMMYYYY**, where **DD** is the two digit day, **MMM** is the abbreviation of the month name (Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sept, Oct, Nov, or Dec), and **YYYY** is the four digit year. Output is a .json file for each screenname, in the format "screenname_tweets.json".

## JSON to CSV Converter - csv_converter.py
The purpose of this program is to take a JSON file of tweets and select the desired attributes to transfer over into a CSV file format.
Below are instructions for the use of this program

### Commands
* **Input File Name:** `-i | --inputfile ` allows the user to indicate what JSON file to input. Only accepts a single input file.

* **Attributes:** `-a | --attributes` allows the user to indicate the desired attributes they want to pull from the JSON file. Default attributes are: id, text, created_at, place, coordinates. **For a list of all possible attributes, see tweet_parts.txt.**

### Execution
```
python csv_converter.py -i user1 -a entities.hashtags.text,text,lang

```
The above command takes the file 'user1.json' as input, and outputs the tweet body text, language, and hashtag text in CSV format with the name 'user1.csv'.

## Classifiers to learn from this dataset

https://github.com/litpuvn/harvey-classifier


## Twitter Error Return Code

https://developer.twitter.com/en/docs/basics/response-codes

## Twitter Tweet Object

**JSON Example:** https://gist.github.com/hrp/900964

**Tweet Object Documentation:** https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object

*Note: There are various kinds of coordinates. 'place', 'coordinates', 'geo'. Place has the capability of telling us where the tweet came from, giving us 4 sets of coordinates that represent a box however it does not neccessarly mean the tweet came from there. Geo is not longer be supported by Twitter. Coordinates, if not null, is the point location of where the tweet came from. Use coordinates, else use place.*

## Authors

Long: https://github.com/litpuvn

Joshua: https://github.com/JStuve

Yusuf: https://github.com/yusufmurat

Christopher: https://github.com/3dchristopher

## Reference

The code is learnt from this blog

https://dev.to/bhaskar_vk/how-to-use-twitters-search-rest-api-most-effectively
