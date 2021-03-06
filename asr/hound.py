# author: kcgarikipati@gmail.com

""" Interface for Hound Speech to Text ASR"""

import wave
import houndify
import sys
import json
import Queue
import argparse
import thread, threading
import utils
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResponseListener(houndify.HoundListener):
    def __init__(self, responseQueue):
        self.responseQueue = responseQueue
    def onPartialTranscript(self, transcript):
        self.responseQueue.put(transcript)
    def onFinalResponse(self, response):
        # self.responseQueue.put(response)
        self.responseQueue.put('EOS')
        # logger.info("Hound finished ")
    def onTranslatedResponse(self, response):
        print "Translated response: " + response
    def onError(self, err):
        self.responseQueue.put('EOS')
        print "Hound ERROR"


def credentials():
    with open("asr/hound_key.json") as f:
        creds_json = json.load(f)
    creds = {}
    creds['CLIENT_ID'] = str(creds_json["ClientID"])
    creds['CLIENT_KEY'] = str(creds_json["ClientKey"])
    return creds

# TODO: Move everything under a single class
def request_stream(client, chunkIterator, responseQueue):
    try:
        finished = False
        for data in chunkIterator:
            # logger.info(len(data))
            if not finished:
                finished = client.fill(data)
        client.finish()
    except:
        responseQueue.put('EOS')
        return


class worker:

    def __init__(self, token):
        self.token = token


    def stream(self, chunkIterator, config=None):

        last_transcript = ''




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-in', action='store', dest='filename', default='audio/test1.raw',
        help='audio file')
    args = parser.parse_args()
    W = worker('123456')
    responses = W.stream(utils.generate_chunks(args.filename, grpc_on=False, chunkSize=3072))
    for response in responses:
        print response