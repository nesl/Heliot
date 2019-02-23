"""
Raspberry Pi Camera
Capturing images
"""

import time
import sys
import pickle

from dataflow import *

#run task will be called with a dataflow object
def run_task():

    print('Running Task Now')
    data = dataflow.getData()
    print('Data is:')
    print(data)

run_task()
