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
import time

class dataflow:

    map_id_op=None
    soc_hel=None
    logs_file = None

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
        #dataflow.logs_file = open('dataflow'+str(time.time())+'.log', "w")
        dataflow.logs_file = open('dataflow'+'.log', "w")

        #harcoding this, we need to get this from master
        dataflow.map_id_op={}
        dataflow.map_id_op['gvt_image_data']='10.0.0.1'#'172.17.15.21'  #ip of tx2
        dataflow.map_id_op['drone_image_data']='172.17.15.21'  #ip of tx2

        dataflow.map_id_op['master']='172.17.15.21'  #ip of master

        #get the pid of the task and send it to the master using socket API



    # We need to send data with id
    @staticmethod
    def sendData(id,data):
        retry=1
        while retry>0:
            try:
                if dataflow.map_id_op==None:
                    dataflow.set_data_input_mapping()

                ip = dataflow.map_id_op[id]

                #maintaing logs on storage
                dataflow.logs_file.write('Sending data to:'+str(ip)+': at time:'+str(time.time()))
                dataflow.logs_file.write('\n')
                dataflow.logs_file.flush()
                dataflow.soc_hel.sendData(ip,data)

                #we don't need to retry now
                retry = 0
                return True

            except Exception as e:
                dataflow.logs_file.write('error on ip:'+str(ip)+': at time:'+str(time.time()))
                dataflow.logs_file.write('\n')
                dataflow.logs_file.write('Exception: '+str(e))
                dataflow.logs_file.write('\n')
                dataflow.logs_file.write('Retry: '+str(retry))
                dataflow.logs_file.write('\n')
                dataflow.logs_file.flush()

                #we will retry again
                retry=retry-1

        return False


    @staticmethod
    def getData(inport=None):
        try:
            if dataflow.map_id_op==None:
                dataflow.set_data_input_mapping()

            #maintaing logs on storage
            dataflow.logs_file.write('getData: at time:'+str(time.time()))
            dataflow.logs_file.write('\n')
            dataflow.logs_file.flush()

            data=dataflow.soc_hel.getData(inport)
            return data

        except Exception as e:
            dataflow.logs_file.write('Error on: getData: at time:'+str(time.time()))
            dataflow.logs_file.write('\n')
            dataflow.logs_file.write(str(e))
            dataflow.logs_file.write('\n')
            dataflow.logs_file.flush()
            return None

# Send the data
