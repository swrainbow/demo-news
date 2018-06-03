from cloudAMQP_client import CloudAMQPClient

CLOUDAMQP_URL = 'amqp://sjtwuuus:1sWbGnYyMJBDjTZG-rjktB7cHteYO-FJ@otter.rmq.cloudamqp.com/sjtwuuus'

TEST_QUEUE_NAME = 'test'

def test_basic():
    client = CloudAMQPClient(CLOUDAMQP_URL,TEST_QUEUE_NAME)

    sentMsg = {'test':'demo'}
    client.sendMessage(sentMsg)
    client.sleep(10)
    receivedMsg = client.getMessage()
    assert sentMsg == receivedMsg
    print 'test_basic passed!'

if __name__ == "__main__":
    test_basic()
