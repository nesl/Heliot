"""
Task: Adds random numbers received
"""

import time
import random
import os, signal
from tasks.utils.dataflow import *

task1_data = []
task2_data = []

#run task will be called with a dataflow object
def run_task():
    file = open("task3.log", "w")
    file.write('Task3 pid is: ' + str(os.getpid()) + "\n")
    file.flush()
    print('Attempting to start task Task3')

    
    try:
        for i in range(10):
            while len(task1_data) == 0 or len(task2_data) == 0: 
                rawdata = dataflow.getData('task3')
                assignData(rawdata)

            data1 = task1_data.pop(0)
            data2 = task2_data.pop(0)

            file.write('Received data' + str(i+1) + ': ' + str(data1) + ', ' + str(data2))
            file.write('\n')
            if data1 != None and data2 != None:
                file.write(str(data1) + ' + ' + str(data2) + ' = ' + str(data1 + data2))
                file.write('\n\n')
            file.flush()

            print('Task3: Received Data:', data1, data2)

    finally:
        file.close()
        os.kill(os.getpid(), signal.SIGTERM)


def assignData(data):
    if data[0] == 'task1_data':
        task1_data.append(data[1])
    elif data[0] == 'task2_data':
        task2_data.append(data[1])
