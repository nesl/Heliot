"""
Task: Multiplies random numbers received
"""

import time
import random
import os, signal

from tasks.utils.dataflow import *

#run task will be called with a dataflow object
def run_task():
    file = open("task4.log", "w")
    file.write('Task4 pid is: ' + str(os.getpid()) + "\n")
    file.flush()
    print('Attempting to start task Task4')

    try:
        for i in range(20):
            data1 = dataflow.getData(9000)
            data2 = dataflow.getData(9000)

            file.write('Received data' + str(i+1) + ': ' + str(data1) + ', ' + str(data2))
            file.write('\n')
            if data1 != None and data2 != None:
                file.write(str(data1) + ' * ' + str(data2) + ' = ' + str(data1 * data2))
                file.write('\n\n')
            file.flush()

            print('Task4: Received Data:', data1, data2)

    finally:
        file.close()
        os.kill(os.getpid(), signal.SIGTERM)

