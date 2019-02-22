# defines the dataflow functionality between tasks

# Running socket send and receive data only on client request.
# No parallel processing of send and receive. Add it as an added option later for users
        # for example sending data behind the computation

# Data: using pickle to send between Tasks
  # ToDO: Extend it to other serializable datatypes and give user option to select the type

# Functionality: Task imports dataflow


#Heliot imports
from utilss.socketHelot import *


class dataflow:

    def __init__(self):
        pass

# Send the data
