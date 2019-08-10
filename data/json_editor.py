print("All input should include preceeding zeroes and have two digit inputs")
month = raw_input("Enter the month: ")
day = raw_input("Enter the day: ")
year = raw_input("Enter the year: ")
string = str(month)+"-"+str(day)+"-" + str(year) + "_0.json"
f = open(string, 'r')
curly = True
list_o_errors = []
x = 0
for i in f:
	x+=1
	num_quotes = 0
	if '{' in i:
		curly = False
		if ('}' in i):
			curly = True
	if '}' in i:
		curly = False
		if ('{' in i):
			curly = True
	if 'created_at' not in i or 'text' not in i or 'tweet_id' not in i or 'region_name' not in i or 'city_name' not in i or 'country_code' not in i or 'user_id' not in i or 'user_name' not in i or 'coordinates' not in i:
		curly = False
	if curly == False:
		print ("Error on line " + str(x))
		list_o_errors.append(x)
print(list_o_errors)
print(x)
