"""
Raspberry Pi Camera
Capturing images
"""

import time
import sys
import pickle
import os

from utils.dataflow import *
filepath = 'local.jpg'

if __name__ == "__main__":
# #There is input port argument
#  if len(sys.argv)!=3:
#   print('usage: python main.py MININET_SERVER_IP MININET_SERVER_PORT')
#   print('Example: python main.py 172.17.20.12 18800')
#   exit(0)
#
#  mininet_ip=str(sys.argv[1])
#  port = int(sys.argv[2])

 camera= picamera.PiCamera()
 camera.resolution = (300, 300)
 #camera.start_preview()

 while True:
  time.sleep(1)
  camera.capture(filepath)
  binary_file=open(filepath, 'rb')
  data = binary_file.read()
  data = base64.b64encode(data)

  result = dataflow.sendData(id='gvt_image_data',data=data)
  print(result)
