import msgpackrpc
import base64
import time
from PIL import Image
import numpy as np
import sys

if __name__ == "__main__":
	
	
	#There is input port argument
	if len(sys.argv)!=2:
		print('usage: python3 test.py PORT_NUM')
		print('Example: python3 test.py 18800')
		exit(0)
	#Parsing the input argument
	port=int(sys.argv[1])

	client = msgpackrpc.Client(msgpackrpc.Address("localhost", port))

	filepath = 'data/image1.jpg'

	#filepath = 'data/Im_rec.png'

	binary_file=open(filepath, 'rb')
	data = binary_file.read()
	data = base64.b64encode(data)
	client = msgpackrpc.Client(msgpackrpc.Address("localhost", 18800))

	while True:
	    result = client.call('push', data, time.time())
	    print(result)
