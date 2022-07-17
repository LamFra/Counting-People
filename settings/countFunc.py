import boto3
import datetime
import json

def lambda_handler(event, context):
	sqs = boto3.resource('sqs', endpoint_url='http://localhost:4566')
	dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

	table = dynamodb.Table('CentroCommercialeCampania')

	shops = ['Carpisa', 'Adidas', 'Carrefour', 'Sephora', 'Zuiki']

	for shop in shops:
		queue = sqs.get_queue_by_name(QueueName=shop)
		messages = []
		while True:
			response = queue.receive_messages(MaxNumberOfMessages=10, VisibilityTimeout=10, WaitTimeSeconds=10)
			if response:
				messages.extend(response)
				num_people = 0
				last_measured_data = datetime.datetime.combine(datetime.date.min, datetime.datetime.min.time())
				for message in messages:
					print(message)
					content = json.loads(message.body)

					measure_data = datetime.datetime.strptime(content["measure_date"], "%Y-%m-%d %H:%M:%S")
					if measure_data > last_measured_data:
						last_measured_data = measure_data
						
						
					if str(content["sensor_type"]) == "in":
						num_people += int(content["people"])
						
					elif str(content["sensor_type"]) == "out":
						num_people -= int(content["people"])
					message.delete()

				
				item = {
					'shop': shop,
					'measure_date': str(last_measured_data), 
					'people': str(num_people)
				}
				table.put_item(Item=item)
			else:
				break	
