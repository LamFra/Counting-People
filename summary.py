import requests
import boto3
import datetime
import json
import datetime 

def lambda_handler(event, context):
	key = "<key>"
	url = "https://maker.ifttt.com/trigger/summary/with/key/"+key
	
	time = 2
	minutes = int('{:02d}'.format(datetime.datetime.now().minute))
	
	if (minutes % time) == 0:
		people = 0
		for record in event['Records']:
			payload = record['body']
			payload = json.loads(str(payload))
			people += int(payload['people1']) - int(payload['people2'])
		average = int(people / time)
		req = requests.post(url, json={"value1": str(average)})
