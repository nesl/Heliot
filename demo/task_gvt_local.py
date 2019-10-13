"""
sending local images
"""

import time
import sys
import pickle
import os
import base64


from utils.dataflow import *
filepath = 'local.jpg'

binary_file=open(filepath, 'rb')
data = binary_file.read()
data = base64.b64encode(data)

result = dataflow.sendData(id='drone_image_data',data=data)
print(result)
