import os
import time
import redis
import json
from threading import Thread
from keyword2text import keyword2text

# Get env vars
REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = os.environ['REDIS_PORT']
print(f'Connecting to {REDIS_HOST}@{REDIS_PORT}')

# Connect to redis
redis_client = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT))
pubsub = redis_client.pubsub()
pubsub.subscribe("keywords")

pubsub_sen = redis_client.pubsub()
pubsub_sen.subscribe(["text"])


def text_result():
    print("Start subcribing.")
    for item in pubsub.listen():
        print("receiving message from js: " + str(item))

        if item["type"] == "message" and item["channel"].decode(
        ) == "keywords":
            data = eval(item["data"].decode())
            print(f"Receiving keywords {data['keywords']}")
            # Publish message when done
            redis_client.publish(
                "text",
                json.dumps({
                    "_id": data["_id"],
                    "textResult": keyword2text(data['keywords']),
                    "status": "testing"
                }))


if __name__ == '__main__':
    print("Worker starts")
    pubsub_thread = Thread(target=text_result, args=())
    pubsub_thread.start()
    pubsub_thread.join()
    print("Worker terminates")