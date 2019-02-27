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

    file = open("taskgvt.txt", "w")
    print('Attempting to run Task GVT')

    for i in range(10):
        file.write(str(i)+': GVK task is running')
        file.write('\n')
        file.flush()

        # filepath = '/home/nesl/Downloads/img.jpg'
        # binary_file=open(filepath, 'rb')
        # data = binary_file.read()
        #print(data)
        data = str(i)+': gvk'
        file.write('Sending data:'+data)
        file.write('\n')
        file.flush()

        result = dataflow.sendData(id='gvt_image_data',data=data)
        print(i,':result is:',result)
        if not result:
            file.write(str(i)+': GVK task data transfer failed')
            file.write('\n')
            file.flush()

        time.sleep(1)
    #print("*"*100)
    #data_string = pickle.dumps(data)
    #print(data_string)

run_task()
