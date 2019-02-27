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
    file = open("tasktx2.txt", "w")
    print('Attempting to start task Tx2')

    for i in range(10):
        print(i, ': Task tx2 is running')
        data = dataflow.getData()

        file.write('Received data:'+str(data))
        file.write('\n')
        file.flush()

        print('Data is:',data)
            #print(data)

        #time.sleep(1)
    file.close()

run_task()
