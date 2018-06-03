# -*- coding: utf-8 -*-

import datetime
import os
import sys

from dateutil import parser
from sklearn.feature_extraction.text import TfidfVectorizer

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
from cloudAMQP_client import CloudAMQPClient

# Use your own Cloud AMQP queue
DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://wmyfoojr:G0ayvBIB7nOlMIdccQvOhpPnSo0Too4B@otter.rmq.cloudamqp.com/wmyfoojr"
DEDUPE_NEWS_TASK_QUEUE_NAME = "tap-news-dedupe-news-task-queue"

SLEEP_TIME_IN_SECONDS = 1

NEWS_TABLE_NAME = "news"

SAME_NEWS_SIMILARITY_THRESHOLD = 0.8

cloudAMQP_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)

def handle_message(msg):
    if msg is None or not isinstance(msg, dict) :
        return
    task = msg
    text = str(task['text'])
    if len(text) < 2:
        text = str(task['title'])
        print '================================================ %s'%(text)
    if text is None:
        print '================================================is none'
        return

    # get all recent news based on publishedAt


while True:
    if cloudAMQP_client is not None:
        msg = cloudAMQP_client.getMessage()
        if msg is not None:
            # Parse and process the task
            try:
                handle_message(msg)
            except Exception as e:
                print e
                pass

        cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)
