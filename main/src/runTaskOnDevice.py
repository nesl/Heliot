#Functionality: running the task on the device
# This file is called on the remote device from the user master computer(computer used to define testbed, scenario etc)

import sys
import importlib
import os

try:
    if len(sys.argv)==2:
        mod = sys.argv[1]
        #import the task file
        file = open("runTaskOnDevice_"+str(mod)+".log", "w")
        file.write('Attempted to start the task')
        file.write('\n')
        file.write('importing task file: ' + str(mod))
        file.write('\n')
        file.flush()

        #print('importing task file')
        mod_task=importlib.import_module('tasks.'+str(mod))
        # mod_task=importlib.import_module('.' + str(mod), package='tasks')
        mod_task.run_task()
        file.close()


except Exception as e:

    file.write('Error:')
    file.write('\n')
    file.write(str(e))
    file.flush()
    file.close()
