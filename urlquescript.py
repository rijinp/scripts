from pymongo import MongoClient
import pika
import json
from time import sleep
import datetime
QUEUE_HOST = 'q details'  # load balancer
QUEUE_USER = 'user name'
QUEUE_PASS = 'password'
QUEUE_NAME = 'ha.name'
DB_NAME = 'db name'
# client = MongoClient()
client = MongoClient('client ip')
db = client[DB_NAME]
COLLECTION_NAME = 'url COLLECTION_NAME'
FIELD = 'url'
FIELD = FIELD.split(',')
FIELD = [x.strip() for x in FIELD if x.strip()]
searchString = {'_id': 1}
for field in FIELD:
    searchString[field] = 1
# searchString = {'url': 1}
print(searchString)
result = db[COLLECTION_NAME].find({}, searchString)
credentials = pika.PlainCredentials(QUEUE_USER, QUEUE_PASS)
connection = pika.BlockingConnection(pika.ConnectionParameters(
    credentials=credentials, host=QUEUE_HOST, socket_timeout=3000))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME, durable=True)
for data in result:
    document = dict(data)
    if len(FIELD) == 1:
        document = document[FIELD[0]]
        channel.basic_publish(
            exchange='', routing_key=QUEUE_NAME, body=document)
        sleep(0.0001)
    else:
        channel.basic_publish(
            exchange='', routing_key=QUEUE_NAME, body=json.dumps(document))
        sleep(0.0001)
connection.close()