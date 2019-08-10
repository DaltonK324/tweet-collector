#!/usr/bin/env python
import time
import subprocess
import datetime
from datetime import date, timedelta


if __name__ == '__main__':


    c = 0
    now = datetime.datetime.now()
    last_time = now.hour
    while(True):
        print("We've been running for " + str(4 * c) + " hours")	
	print("last_time = " + str(last_time))
	print("now.hour = " + str(now.hour))
        now = datetime.datetime.now()
        c = c+1
	subprocess.call("python live.py", shell=True)	
	if (now.hour < last_time):
		yesterday = (datetime.datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
		yesterday_fstring = str(yesterday[5:7]) + "-" + str(yesterday[8:10]) + "-" + str(yesterday[2:4]) + "_0."
		subprocess.call("cd data; tar -czf " + yesterday_fstring + "tar.gz " + yesterday_fstring + "json", shell = True)
		print("File for " + yesterday_fstring + "Successfully compressed.")
		subprocess.call("cd data; rm " + yesterday_fstring + "json", shell = True)
		print("Json file for " + yesterday_fstring + "Successfully removed.")
	last_time = now.hour			
