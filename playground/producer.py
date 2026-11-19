import json
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='test.queue', durable=True)

message = {'job_id': 'job-0010', 'text': 'abc from Python'}

channel.basic_publish(
    exchange='',
    routing_key='test.queue',
    body=json.dumps(message),
)

print('Sent:', message)

connection.close()