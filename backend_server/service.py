import pyjsonrpc
import json
import os
import sys
import operations

from bson.json_util import dumps

sys.path.append(os.path.join(os.path.dirname(__file__),'..','common'))
import mongodb_client
SERVICE_HOST = 'localhost'
SERVICE_PORT = 4040

class RequestHandler(pyjsonrpc.HttpRequestHandler):
    """Test Methos"""
    @pyjsonrpc.rpcmethod
    def add(self,a,b):
        print "add is called with %d and %d" % (a,b)
        return a + b

    @pyjsonrpc.rpcmethod
    def getNewsSummariesForUser(self,user_id,page_num):
        return operations.getNewsSummariesForUser(user_id,page_num)

    @pyjsonrpc.rpcmethod
    def logNewsClickForUser(self,user_id,news_id):
        return operations.logNewsClickForUser(user_id,news_id)

http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = (SERVICE_HOST,SERVICE_PORT),
    RequestHandlerClass = RequestHandler
)

print "Starting HTTp server on %s:%d"%(SERVICE_HOST,SERVICE_PORT)

http_server.serve_forever()
