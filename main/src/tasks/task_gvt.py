"""
Raspberry Pi Camera
Capturing images
"""

import time
import sys
import pickle
import os

from .dataflow import *

#run task will be called with a dataflow object
def run_task():

    file = open("taskgvt.txt", "w")

    for i in range(100):
        print('Running Task Now')
        file.write(str(i)+': Task is running')
        file.write('\n')
        file.flush()

        filepath = '/home/nesl/Downloads/img.jpg'
        binary_file=open(filepath, 'rb')
        data = binary_file.read()
        #print(data)
        dataflow.sendData(id='gvt_image_data',data=data)
        time.sleep(1)
    #print("*"*100)
    #data_string = pickle.dumps(data)
    #print(data_string)

#run_task()
