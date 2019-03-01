"""
Raspberry Pi Camera
Capturing images
"""

import time
import sys
import pickle
import os

from dataflow import *

#run task will be called with a dataflow object
def run_task():
    print('Attempting to run Task')

    for i in range(100):

        data = str(i)+': gvk'
        result = True

        result = dataflow.sendData(id='gvt_image_data',data=data)
        print(i,':result is:',result)
        time.sleep(1)
        
run_task()
