"""
Raspberry Pi Camera
Capturing images
"""

import time
import sys
import pickle
import os
import picamera
import base64


from utils.dataflow import *
filepath = 'local.jpg'

if __name__ == "__main__":
 camera= picamera.PiCamera()
 camera.resolution = (300, 300)
 #camera.start_preview()

 while True:
  time.sleep(0.5)
  try:
    camera.capture(filepath)
    binary_file=open(filepath, 'rb')
    data = binary_file.read()
    data = base64.b64encode(data)

    result = dataflow.sendData(id='gvt_image_data',data=data)
    print(result)
  except Exception as e:
    print(e)
