#!/usr/bin/env python
import pika
from os import getenv
from time import sleep
from datetime import datetime
from json import loads

username = getenv("RMQ_USERNAME", "guest")
password = getenv("RMQ_PASSWORD", "guest")
host = getenv("RMQ_HOST")
port = getenv("RMQ_PORT", "5672")
vhost = getenv("RMQ_VHOST", "/")
queue = getenv("RMQ_QUEUE")
consumer_tag = getenv("RMQ_CONSUMER_TAG", "test-consumer")


def on_message(channel, method_frame, header_frame, body):
    try:
        tmp_body = loads(body)
        sleep(tmp_body["sleep_seconds"])
        print("{} - {}".format(method_frame.delivery_tag, body), flush=True)
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
    except Exception as e:
        print(e, flush=True)


while True:
    try:
        credentials = pika.PlainCredentials(username, password)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host, port=port, virtual_host=vhost, credentials=credentials
            )
        )
        channel = connection.channel()
        channel.basic_qos(prefetch_count=1000)
        channel.basic_consume(queue, on_message, consumer_tag=consumer_tag)
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
            connection.close()
            break

    except (
        pika.exceptions.ConnectionClosedByBroker,
        pika.exceptions.AMQPConnectionError,
    ):
        print("Connection was closed, retrying...", flush=True)
        continue
    except pika.exceptions.AMQPChannelError as err:
        print("Caught a channel error: {}, stopping...".format(err), flush=True)
        break
    except pika.exceptions.AMQPConnectionError:
        print("Connection was closed, retrying...", flush=True)
        continue

connection.close()
