"""
Raspberry Pi Camera
Capturing images
"""


import msgpackrpc
import base64
import time
import picamera

filepath = 'local.jpg'


camera= picamera.PiCamera()
camera.resolution = (300, 300)
#camera.start_preview()


while True:
 time.sleep(1)
 camera.capture(filepath)
 binary_file=open(filepath, 'rb')
 data = binary_file.read()
 data = base64.b64encode(data)
 client = msgpackrpc.Client(msgpackrpc.Address("172.17.49.60", 18800))
 result = client.call('push', data, time.time())
 print(result)
