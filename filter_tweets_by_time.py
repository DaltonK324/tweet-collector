import csv
from datetime import datetime

filter_by = 'month'

tweets_by_time = dict()

headerLine = None

with open('tweets/twdb_tweets.csv', mode='r') as csvfile:
    tweetLines = csv.reader(csvfile)
    header = True
    for line in tweetLines:

        if header == True:
            header = False
            headerLine = line
            continue

        time = line[2]
        # myDateTime = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
        myDateTime = datetime.strptime(time, '%a %b %d  %H:%M:%S +%f %Y')
        monthYear = myDateTime.strftime('%Y-%m')
        if monthYear not in tweets_by_time:
            tweets_by_time[monthYear] = []
        # csvLine = ','.join(line)
        tweets_by_time[monthYear].append(line)


for time, tweets_at_time in tweets_by_time.items():
    with open('output/' + time + '.csv', 'w') as o:
        # writer = csv.writer(o)
        writer = csv.DictWriter(o, fieldnames=headerLine)
        writer.writeheader()

        # writer.writerow(headerLine)
        for line in tweets_at_time:
            writer.writerow({headerLine[i]: line[i] for i in range(len(line))})

print('done')