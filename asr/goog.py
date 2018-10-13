# author: kcgarikipati@gmail.com


""" Interface for Google Cloud Speech ASR"""

#from google.cloud import speech as cloud_speech
#from google.cloud.speech import enums
#from google.cloud.speech import types

from google.rpc import code_pb2
import time, random
import argparse
import utils, sys
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Audio recording parameters
RATE = 16000


class worker:

	def __init__(self, token):
		self.got_end_audio = False
		self.token = token


	def request_stream(self, chunkIterator):

		for data in chunkIterator:
			logger.debug("%s: sending to google = %d", self.token, len(data))
			if self.got_end_audio:
				raise StopIteration
			else:
				yield 1
					#types.StreamingRecognizeRequest(audio_content=data)


	def stream(self, chunkIterator, config=None):

		is_final = False
		last_transcript = ''
		last_confidence = -1
		continuous_transcript = [''] # list of multiple is_final sub-transcripts
		logger.debug("%s: sending to google = %d",str(chunkIterator))
		self.request_stream(chunkIterator)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-in', action='store', dest='filename', default='audio/test1.raw', help='audio file')
	args = parser.parse_args()
	config = {
	"language": "en-US",
	"encoding":"LINEAR16",
	"sampling_rate":RATE,
	"max_alternatives":5,
	"interim_results": True,
	"profanity_filter": True,
	"continuous": False,
	}

	W = worker('123456')
	responses = W.stream(utils.generate_chunks(args.filename, grpc_on=False, chunkSize=3072),
		config)
	#for response in responses:
	#	print response