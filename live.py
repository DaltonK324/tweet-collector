import os
import re
import unicodedata
import sys
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import datetime
import argparse
import config

def get_parser():
	parser = argparse.ArgumentParser(description="Twitter Downloader")
	parser.add_argument("-ln", "--lang", dest="language", help="Language", default = "en")
	parser.add_argument("-c", "--country", dest="country", help="Country/Alpha-2 Coding (US, UK, MX, ..)", default="US")
	parser.add_argument("-q", "--query", dest="query", help="Query/Filter", default="-")
	parser.add_argument("-d", "--data-dir", dest="data", help="Output/Data Directory", default=str(os.getcwd() + "/data"))
	return parser



class MyListener(tweepy.StreamListener):
	curDir = ""
	fileNumber = 0
	currentDay = datetime.date.today().strftime('%m-%d-%y')
	tweetCount = 0
	timer = (60) * 30 # thirty minutes
	endTimer = (60 * 60) * 4 # four hours
	endProc = False
	endProcTime = 0
	outfile = ''
	MAX_SIZE = 200000000
	endTime = 0
	flushTimer = 60*20 # twenty minutes
	flushEnd = 0

	def __init__(self, data_dir):
		self.endProcTime = time.time() + self.endTimer
		self.curDir = data_dir
		self.set_file_name(self.curDir)
		self.timer_check()
		self.flush_file()
	def flush_file(self):
		if(time.time() > self.flushEnd):
			file = open(self.outfile, 'a')
			file.flush()
			file.close()
		self.flushStart = time.time()
		self.flushEnd = self.flushStart + self.flushTimer
		return
	def timer_check(self):
		if(time.time() > self.endTime):
			print('{} Tweets, recorded at {}'.format(self.tweetCount, datetime.datetime.now()))
			self.startTime = time.time()
			self.endTime = self.startTime + self.timer
			self.tweetCount = 0
		if(time.time() > self.endProcTime):
			self.endProc = True
			
		return
	def on_data(self,data):
		if(self.endProc is True):
			return True
		if isinstance(data,unicode):
			data = data.encode('utf-8')
		if ('"text":' in data):
			split_on_text = data.split('"text":')
		else:
			return
		split_on_id = split_on_text[0].split("id")		
		created_at_string = data[14:45]
		created_at_string = created_at_string.replace('"','')
		id_tweet_string = split_on_id[1][2:len(split_on_id[1])-2]
		
		split_after_text = re.split(',"display_text_range":|","source":"', split_on_text[1])
		text_string = split_after_text[0][1:]
		text_string = text_string.replace('"','')
		text_string = text_string.replace("'",'')
		text_string = text_string.replace('/','')
		text_string = repr(text_string)

		split_on_user = split_after_text[1].split('"user":{')
		split_on_user_id_str = split_on_user[1].split('"id_str":"')
		id_user_string = split_on_user_id_str[0][5:len(split_on_user_id_str[0])-1]
		split_on_user_name = re.split('"name"|"screen_name"',split_on_user_id_str[1])
		user_name_string = (split_on_user_name[1][2:len(split_on_user_name[1])-2])

		if ('"place":{' in data and '"place":null' not in data):		
			split_on_place = split_after_text[1].split('"place":{')
			split_on_place_name_country = re.split('"full_name"|"country_code"',split_on_place[1])		
			region_name_string = (split_on_place_name_country[1][2:len(split_on_place_name_country[1])-2])		
			split_on_place_type = re.split('"place_type"', split_on_place_name_country[0])			
			#Checking for an edge case where the country code was not in the tweet even if the place was not null.			
			if (split_on_place_name_country[2][2:4] == '",'):
				place_country_string = 'None'
			else:	
				place_country_string = split_on_place_name_country[2][2:4]
			split_on_coordinates = re.split('"coordinates"|"attributes"', split_on_place_name_country[2])
			coordinates_string = (split_on_coordinates[1][2:len(split_on_coordinates[1])-3])
			if (split_on_place_type[1][2] is 'c'):
				place_city_string = split_on_place_type[1][16:len(split_on_place_type[1])-2]		
			else:
				place_city_string = 'None'
			if (place_city_string is not 'None'):
				split_on_region = re.split(',', split_on_place_name_country[1])
				region_name_string = split_on_region[1][1:len(split_on_region[1])-1]
			else:
				split_place_admin = re.split(":", split_on_place_type[1])
				region_name_string = split_place_admin[2][1:len(split_place_admin[2])-2]	
		else:
			region_name_string = 'None'
			place_country_string = 'None'
			coordinates_string = '"None"'
			place_city_string = 'None'
		
		string_to_print = ('{"created_at": "' + created_at_string + '", "tweet_id": '  + id_tweet_string + ', "text": "' + text_string + '", "user_id": ' + id_user_string + ', "user_name": "' + user_name_string + '", "region_name": "' + region_name_string + '", "city_name": "' + place_city_string + '", "country_code": "' + place_country_string + '", "coordinates": ' + coordinates_string + '}\n')		
		try:
			self.set_file_name(self.curDir)
			with open(self.outfile, 'a') as f:
				f.write(string_to_print)
				self.tweetCount = self.tweetCount + 1
				self.timer_check()
				self.flush_file()
			return True
		except BaseException as e:
			print("Error on_data: %s" % str(e))
			time.sleep(5)
		return True


	def on_error(self, status):
		print(self.curDir)
		if (status == 401):
			print("401 - Unauthorized: Missing or incorrect authentication credentials. This may also returned in other undefined circumstances.")
		elif(status == 400):
			print("400 - Bad Request: The request was invalid or cannot be otherwise served. An accompanying error message will explain further. Requests without authentication are considered invalid and will yield this response.")
		elif(status == 403):
			print("403 - Forbidden: The request is understood, but it has been refused or access is not allowed. An accompanying error message will explain why. This code is used when requests are being denied due to update limits .")
		elif(status == 429):
			print("429 - Too Many Requests: Returned when a request cannot be served due to the applications rate limit having been exhausted for the resource.")
		else:
			print("Error Code: " + status + ", check README for link to all the codes.")
		return True
	def set_file_name(self, data_dir):
		if(self.currentDay != datetime.date.today().strftime('%m-%d-%y')):			
			self.currentDay = datetime.date.today().strftime('%m-%d-%y')
			self.fileNumber = 0
			print("New File Created: {}_{}.json".format(self.currentDay, self.fileNumber))
		else:
			filePath = '{}\\{}_{}.json'.format(data_dir, self.currentDay, self.fileNumber)			
			if(os.path.isfile(filePath)):
				if(os.path.getsize(filePath) >= self.MAX_SIZE):
					self.fileNumber = self.fileNumber + 1
					print("New File Created: {}_{}.json".format(self.currentDay, self.fileNumber))
			self.outfile = "{}/{}_{}.json".format(data_dir, self.currentDay, self.fileNumber)



if __name__ == '__main__':	
	US = [-130.42,27.2,-59.33,49.68,-158.9,15.7,-151.5,22.3,-169.3,54.6,-141.0,71.4]
	UK = [-5.59,49.48,1.76,59.43]
	FR = [-5.08,42.07,7.73,50.03]
	GR = [6.6,48.43,13.97,54.88]
	MX = [-119.28,15.2,-91.23,30.97]    
	countryCord = {"US": US, "UK": UK, "FR": FR, "GR": GR, "MX": MX}

	parser = get_parser()
	args = parser.parse_args()
	
	l = MyListener(args.data)
	auth = OAuthHandler(config.consumer_key, config.consumer_secret)
	auth.set_access_token(config.access_token, config.access_secret)	
	try:
		stream = Stream(auth, l)
		stream.filter(track=[args.query], languages=[args.language], locations=countryCord[args.country])	
	except:
		print("Error: " + str(sys.exc_info()))
