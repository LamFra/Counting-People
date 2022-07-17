from pprint import pprint
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

table_name = "CentroCommercialeCampania"

print("Welcome into the CountingPeople application.")
print("Enter the name of one or more shops you want to know the number of people within it")
shops = input("(shops must be separated by one space):\n")
shops = shops.split()
table = dynamodb.Table(table_name)
print("------------------------------------------------------------------------------------------------")
for shop in shops:
	try:
		response = table.get_item(Key={'shop': shop})
	except ClientError as e:
		print(e.response['Error']['Message'])

	print("Number of people in %s is %s"
		% (response['Item']['shop'], response['Item']['people']))
	print("-measured at %s" 
		% (response['Item']['measure_date']))
	print("------------------------------------------------------------------------------------------------")
