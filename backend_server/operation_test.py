import operations
import os
import sys

from sets import Set

sys.path.append(os.path.join(os.path.dirname(__file__),'..','common'))

import mongodb_client
from cloudAMQP_client import CloudAMQPClient

LOG_CLICKS_TASK_QUEUE_URL ="amqp://ohrfsoad:t4YVuruBTMBrE4r7o0jeZ6N4oqNnUKqB@otter.rmq.cloudamqp.com/ohrfsoad"
LOG_CLICKS_TASK_QUEUE_NAME = "tap-news-log-clicks-task-queue"

CLICK_LOGS_TABLE_NAME = 'click_logs'

cloudAMQP_client = CloudAMQPClient(LOG_CLICKS_TASK_QUEUE_URL,LOG_CLICKS_TASK_QUEUE_NAME)


def test_logNewsClickForUser_basic():
    db = mongodb_client.get_db()
    db[CLICK_LOGS_TABLE_NAME].delete_many({"userId":"test"})

    operations.logNewsClickForUser('test','test_news')

    record = list(db[CLICK_LOGS_TABLE_NAME].find().sort([('timestamp',-1)]).limit(1))[0]

    assert record is not None
    assert record['userId'] == 'test'
    assert record['newsId'] == 'test_news'
    assert record['timestamp'] is not None

    db[CLICK_LOGS_TABLE_NAME].delete_many({"userId":"test"})

    msg = cloudAMQP_client.getMessage()
    assert msg is not None

    print 'test_logNewsClickForUser_basic passed!!'


if __name__ == "__main__":
    test_logNewsClickForUser_basic();
