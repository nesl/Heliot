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
    for i in range(100):
        try:
            file.write(str(i)+': Task is running')
            file.write('\n')
            file.flush()


            print('Running Task Now')
            data = dataflow.getData()
            #print('Data is:')
            #print(data)

        except Exception as e:
            print('Exception:',e)

        time.sleep(1)
    file.close()

#run_task()
