# defines the dataflow functionality between tasks

# Running socket send and receive data only on client request.
# No parallel processing of send and receive. Add it as an added option later for users
        # for example sending data behind the computation

# Data: using pickle to send between Tasks
  # ToDO: Extend it to other serializable datatypes and give user option to select the type

# Functionality: Task imports dataflow

"""
Uses socketHeliot function
sendData: requires the ip, port of the machine to which to send data.
This required information is send by the master to the each node in the testbed.
"""
#Heliot imports
from .socketHeliot import *


class dataflow:

    map_id_op=None
    soc_hel=None

    def __init__(self):
        pass

    # We need to set mapping of id and ip
    #id is the data input which any task may need
    #ip is the ip of the device where there is running.

    #On the machine which task is running, there is a socket receive function is running

    @staticmethod
    def set_data_input_mapping():

        # We need to decide an appropriate place to put it
        dataflow.soc_hel = socketHeliot()

        #harcoding this, we need to get this from master
        dataflow.map_id_op={}
        dataflow.map_id_op['gvt_image_data']='172.17.15.21'  #ip of tx2
        dataflow.map_id_op['drone_image_data']='172.17.15.21'  #ip of tx2

    # We need to send data with id
    @staticmethod
    def sendData(id,data):
        try:
            if dataflow.map_id_op==None:
                dataflow.set_data_input_mapping()

            ip = dataflow.map_id_op[id]
            print('Sending data to:',ip)

            dataflow.soc_hel.sendData(ip,data)
        except Exception as e:
            print(e)

    @staticmethod
    def getData():
        try:
            if dataflow.map_id_op==None:
                dataflow.set_data_input_mapping()

            data=dataflow.soc_hel.getData()
            return data

        except Exception as e:
            print(e)

# Send the data
