<div id="top"></div>

# CountingPeople application
## Introduction
Counting People is a simulator that counts the total number of people 
inside the main shops of the "_Campania_" _shopping centre_. The project is based on an IoT Cloud architecture in which several IoT sectors 
(an entry and exit sensor for each shop considered) collect data and send them 
to the Cloud where they are processed via Serverless Computing and stored in 
a NoSQL database. 

### Structure 

The IoT sensors are structured as follows:
- for each shop considered there is a sensor at the entrance door capable of detecting when a person enters and another 
at the exit door capable of detecting when a person leaves the shop.

<p align="right">(<a href="#top">back to top</a>)</p>

## Architecture

![architecture](https://github.com/LamFra/CountingPeople/blob/main/img/architecture.PNG?raw=true)

The purpose of this project is to indicate the 
number of people inside a shop in order to never exceed the maximum threshold allowed for each shop. 
Each sensor (entry and exit) sends a message with the number of persons detected to the queue for its shop.
Every minute, a time-triggered Servereless function calculates the total number of people for each main shop
using the messages stored in the queues. For each queue, the function collects
the number of people detected by the entry and exit sensors and calculates 
the total number of those inside each shop, then uploads the result to a NoSQL 
database.

<p align="right">(<a href="#top">back to top</a>)</p>

## Installation
### Prerequisites

* [Docker](https://docs.docker.com/get-docker/)
* [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
* [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html)

<p align="right">(<a href="#top">back to top</a>)</p>

### Getting Started

1. Clone the repository
   ```sh
   git clone https://github.com/LamFra/CountingPeople.git
   ```
2. Launch LocalStack
   ```sh
   docker run --rm -it -p 4566:4566 -p 4571:4571 localstack/localstack
   ```
3. Create a SQS queue for each shop
   ```sh
   aws sqs create-queue --queue-name Carpisa --endpoint-url=http://localhost:4566
   ```   
    ```sh
   aws sqs create-queue --queue-name Adidas --endpoint-url=http://localhost:4566
   ```  
    ```sh
   aws sqs create-queue --queue-name Zuiki --endpoint-url=http://localhost:4566
   ```  
    ```sh
   aws sqs create-queue --queue-name Carrefour --endpoint-url=http://localhost:4566
   ```  
    ```sh
   aws sqs create-queue --queue-name Sephora --endpoint-url=http://localhost:4566
   ```  
4. Create the DynamoDB table
   ```sh
   python3 settings/createTable.py
   ``` 
5. Populate the tables with initial data
    ```sh
   python3 settings/loadData.py
   ``` 
- Check the value of the entire database with populate tables
    ```sh
   aws dynamodb scan --table-name Campania --endpoint-url=http://localhost:4566
   ``` 
6. Create the time-triggered Lambda function to count the total number of people within each shop
- Create the role and attach the policy  
    ```sh
  aws iam create-role --role-name lambdarole --assume-role-policy-document file://settings/role.json --query 'Role.Arn' --endpoint-url=http://localhost:4566
   ``` 
    ```sh
  aws iam put-role-policy --role-name lambdarole --policy-name lambdapolicy --policy-document file://settings/policy.json --endpoint-url=http://localhost:4566
   ``` 
- Create the zip file
   ```sh
  zip countFunc.zip settings/countFunc.py
   ``` 
- Create the lambda function and save the Arn
    ```sh
  aws lambda create-function --function-name countFunc --zip-file fileb://countFunc.zip --handler countFunc.lambda_handler --runtime python3.6 --role arn:aws:iam::000000000000:role/lambdarole --endpoint-url=http://localhost:4566
   ``` 
- Test the function with a simulation of IoT Devices and invoke manually the function
    ```sh
  python3 IoTDevices.py
   ``` 
    ```sh
  aws lambda invoke --function-name countFunc --payload fileb://settings/shop.json out --endpoint-url=http://localhost:4566
   ``` 
7. Set up a rule to trigger the Lambda function every minute
- Create the rule and save the Arn
    ```sh
  aws events put-rule --name calculateAvg --schedule-expression 'rate(1 minutes)' --endpoint-url=http://localhost:4566
   ``` 
- Add permissions to the rule 
    ```sh
  aws lambda add-permission --function-name countFunc --statement-id calculateNumPeople --action 'lambda:InvokeFunction' --principal events.amazonaws.com --source-arn arn:aws:events:us-east-2:000000000000:rule/countFunc --endpoint-url=http://localhost:4566
   ```
- Add the lambda function to the rule using the JSON file 
   ```sh
  aws events put-targets --rule calculateNumPeople --targets file://target.json --endpoint-url=http://localhost:4566
   ``` 
_Now every minute the function countFunc will be triggered._

<p align="right">(<a href="#top">back to top</a>)</p>


## Usage
1. Simulate the devices
    ```sh
   python3 IoTDevices.py
    ```
2. Wait or invoke Lambda function manually
   ```sh
   python3 getPeople.py
    ```
The output should be more similar to this: 


<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Francesca La Manna - lamannafrancesca.flm@gmail.com

Project Link: [https://github.com/LamFra/CountingPeople](https://github.com/LamFra/CountingPeople)

<p align="right">(<a href="#top">back to top</a>)</p>
