#Functionality: running the task on the device
# This file is called on the remote device from the user master computer(computer used to define testbed, scenario etc)

import sys
import importlib

# modify to read in the command line arguments

if len(sys.argv)==2:

    mod = sys.argv[1]
    
    #import the task file
    print('importing task file')
    mod_task=importlib.import_module('tasks.'+str(mod))
    mod_task.run_task()
