import pika
import time
from flask import Flask, request, jsonify
import mysql.connector
import json
from flask_pymongo import PyMongo
import pymongo
from pymongo.mongo_client import MongoClient
import socket
import certifi

app = Flask(__name__)   

uri = ""

client = MongoClient(uri,tlsCAFile=certifi.where())
db = client['studentdb']
collection = db["student"]

# def callback(ch, method, properties, body):
#     srn = json.loads(body)['srn']

#     mydb = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="password",
#         database="students"
#     )

#     mycursor = mydb.cursor()

#     sql = "DELETE FROM student WHERE srn = %s"
#     val = (srn, )

#     mycursor.execute(sql, val)

#     mydb.commit()

#     print(f"Deleted record with SRN={srn} from the database")

#     ch.basic_ack(delivery_tag=method.delivery_tag)


sleepTime = 20
time.sleep(sleepTime)
print('Consumer_three connecting to server ...')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='delete_record', durable=True)

def callback(ch, method, properties, body):
    b = body.decode()
    collection.delete_one({"SRN":b})
    ch.basic_ack(delivery_tag=method.delivery_tag)
    return "Student deleted successfully!"
    
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='delete_record', on_message_callback=callback)
channel.start_consuming()