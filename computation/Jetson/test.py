import msgpackrpc
import base64
import time
from PIL import Image



client = msgpackrpc.Client(msgpackrpc.Address("localhost", 18800))

filepath = 'data/image1.jpg'

binary_file=open(filepath, 'rb')
data = binary_file.read()
data = base64.b64encode(data)
client = msgpackrpc.Client(msgpackrpc.Address("localhost", 18800))

while True:
    result = client.call('runInference', data, time.time())
    print(result)
