import pika
import time
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import socket
import certifi
import pymongo
import pymysql
from pymongo.mongo_client import MongoClient

app = Flask(__name__)

uri = ""


client = MongoClient(uri,tlsCAFile=certifi.where())
db = client['studentdb']
collection = db["student"]

# def insert_data(body):
#     data = body.decode('utf-8').split(",")
#     name = data[0]
#     srn = data[1]
#     section = data[2]

#     # MySQL Connection
#     mysql_conn = pymysql.connect(host='database',
#                                 user='root',
#                                 password='password',
#                                 db='students')

#     mysql_cursor = mysql_conn.cursor()
#     insert_query = f"INSERT INTO student (name, srn, section) VALUES ('{name}', '{srn}', '{section}')"
#     mysql_cursor.execute(insert_query)
#     mysql_conn.commit()
#     mysql_conn.close()


sleepTime = 20
time.sleep(sleepTime)
print('Consumer_two connecting to server ...')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='insert_record', durable=True)

def callback(ch, method, properties, body):
    b = body.decode()
    b1 = b.split(".")
    x = b1[0]
    y = b1[1]
    z = b1[2]
    dict1 = {"SRN": x,"Name":y,"Section":z}
    collection.insert_one(dict1)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    return "Student saved successfully!"
    


channel.basic_qos(prefetch_count=1) #always

channel.basic_consume(queue='insert_record', on_message_callback=callback)
channel.start_consuming()