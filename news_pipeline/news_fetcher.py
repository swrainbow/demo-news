# -*- coding: utf-8 -*-

import os
import sys
from newspaper import Article



# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

import cnn_news_scraper
from cloudAMQP_client import CloudAMQPClient

# Use your own Cloud AMQP queue
DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://wmyfoojr:G0ayvBIB7nOlMIdccQvOhpPnSo0Too4B@otter.rmq.cloudamqp.com/wmyfoojr"
DEDUPE_NEWS_TASK_QUEUE_NAME = "tap-news-dedupe-news-task-queue"
SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://sjtwuuus:1sWbGnYyMJBDjTZG-rjktB7cHteYO-FJ@otter.rmq.cloudamqp.com/sjtwuuus"
SCRAPE_NEWS_TASK_QUEUE_NAME = "tap-news-scrape-news-task-queue"

SLEEP_TIME_IN_SECONDS = 5

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

def handle_message(msg):
    if msg is None or not isinstance(msg,dict):
        print 'message is broken'
        return
    task = msg

    article = Article(task['url'])
    article.download()
    article.parse()

    print "======================%s "%(article.text)
    task['text'] = article.text
    dedupe_news_queue_client.sendMessage(task)


while True:
    #fetch msg from queue_name
    if scrape_news_queue_client is not None:
        msg = scrape_news_queue_client.getMessage()
        if msg is not None:
            try:
                handle_message(msg)
            except Exception as e:
                print e
                pass
        scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)
    #handle Message
