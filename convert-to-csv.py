import json, csv
import codecs
import sys
reload(sys)

sys.setdefaultencoding('utf8')

def convert_one_file(filePath):
    with codecs.open(filePath, 'r') as data_file:
        outputFile = filePath[0:(len(filePath)-3)]

        with codecs.open(outputFile + '.csv', 'w') as outF:
            fieldnames = ['User ID', 'Text', 'Location', 'Time Stamp']
            writer = csv.DictWriter(outF, fieldnames=fieldnames)
            writer.writeheader()

            for line in data_file:
                jsonData = json.loads(line)
                writer.writerow({'User ID': str(jsonData["user"]["id"]),
                              'Text': jsonData["text"],
                              'Location': jsonData["user"]["location"],
                              'Time Stamp': jsonData["created_at"]
                              })





