#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials('justry', '123456')

connection = pika.BlockingConnection(pika.ConnectionParameters(host='test-XPS-8920', credentials=credentials))
channel = connection.channel()


channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()