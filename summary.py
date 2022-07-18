import requests
import boto3
import datetime
import json
import datetime 

def lambda_handler(event, context):
	key = "dWAGFb78ji-b29CmAe44TF"
	url = "https://maker.ifttt.com/trigger/summary/with/key/"+key
	
	minutes = int('{:02d}'.format(datetime.datetime.now().minute()))
	
	if minutes == 0:
		people = 0
		for record in event['Records']:
			payload = record['body']
			payload = json.loads(str(payload))
			people += int(payload['people1']) - int(payload['people2'])
		average = int(people / 60) 
		req = requests.post(url, json={"value1": average})
