#Functionality: running the task on the device
# This file is called on the remote device from the user master computer(computer used to define testbed, scenario etc)

import sys
import importlib
import os

file = open("runTaskOnDevice.log", "w")

try:
    if len(sys.argv)==2:
        mod = sys.argv[1]
        #import the task file
        file.write('Attempted to start the task')
        file.write('\n')
        file.write('importing task file')
        file.write('\n')
        file.flush()

        print('importing task file')
        mod_task=importlib.import_module('tasks.'+str(mod))
        mod_task.run_task()



except Exception as e:

    file.write('Error:')
    file.write('\n')
    file.write(str(e))
    file.flush()
