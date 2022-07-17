import boto3
import datetime
import random

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

table = dynamodb.Table('CentroCommercialeCampania')

shops = [('Carpisa', 5), ('Adidas', 8), ('Carrefour', 6), ('Sephora', 7), ('Zuiki', 8)]


for i in range(len(shops)):
    measure_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    people = random.randint(0, shops[i][1])
    item = {
        'shop': shops[i][0],
        'measure_date': str(measure_date), 
        'people': str(people)
    }
    table.put_item(Item=item)

    print("Stored item", item)
