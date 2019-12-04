"""
Task: Send 10 random numbers between 0 and 10
"""

import time
import random
import sys
import os


from tasks.utils.dataflow import *
# from utils.dataflow import *

# Run task will be called with a dataflow object
def run_task():
    print('Attempting to run Task2')
    file = open("task2.log", "w")

    try: 
        for i in range(10):
            data = random.randint(0, 10)

            result = dataflow.sendData(id='task2_data', data=data)
            print('Task2(' + str(i) + '): Sending', data, ":", result)
            file.write('Task2(' + str(i) + '): Sending ' + str(data) + " : " + str(result))
            file.write('\n')
            file.flush()

            time.sleep(1)

    finally:
        file.close()

