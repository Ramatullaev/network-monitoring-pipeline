import json
import time
import pika

def on_message(chnnel, method, properties, body):
    message = json.loads(body)
    print('Received:', message)

    time.sleep(3)
    print('Done with', message['job_id'])

    channel.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='test.queue', durable=True)

channel.basic_consume(queue='test.queue', on_message_callback=on_message)

print('Waiting for messages. Press Ctrl+C to stop.')
channel.start_consuming()
