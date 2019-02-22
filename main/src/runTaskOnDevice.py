#Functionality: running the task on the device
# This file is called on the remote device from the user master computer(computer used to define testbed, scenario etc)

import sys
import importlib

# modify to read in the command line arguments

#import the task file
print('importing task file')
mod_task=importlib.import_module('tasks.'+'task_gvt')
mod_task.run_task()
