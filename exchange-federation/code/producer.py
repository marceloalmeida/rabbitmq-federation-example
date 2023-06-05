#!/usr/bin/env python
import pika
from os import getenv
from time import sleep
from datetime import datetime
from json import dumps
from random import uniform

username = getenv("RMQ_USERNAME", "guest")
password = getenv("RMQ_PASSWORD", "guest")
host = getenv("RMQ_HOST")
port = getenv("RMQ_PORT", "5672")
vhost = getenv("RMQ_VHOST", "/")
exchange = getenv("RMQ_EXCHANGE")
routing_key = getenv("RMQ_ROUTING_KEY")
provider_region = getenv("RMQ_PROVIDER_REGION")

while True:
    try:
        credentials = pika.PlainCredentials(username, password)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host, port=port, virtual_host=vhost, credentials=credentials
            )
        )
        channel = connection.channel()
        channel.confirm_delivery()
    except KeyboardInterrupt:
        connection.close()
        break
    except (
        pika.exceptions.ConnectionClosedByBroker,
        pika.exceptions.AMQPConnectionError,
    ):
        continue

    while True:
        sleep_seconds = uniform(
            float(getenv("MIN_SLEEP", 0)), float(getenv("MAX_SLEEP", 2))
        )
        channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=dumps(
                {
                    "header": provider_region,
                    "sleep_seconds": sleep_seconds,
                    "routing_key": routing_key,
                    "time": datetime.now().strftime("%Y/%m/%d - %H:%M:%S:%f"),
                }
            ),
        )
        sleep(sleep_seconds)


connection.close()
