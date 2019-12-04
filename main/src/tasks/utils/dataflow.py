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
import json


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
    def set_data_input_mapping(id, get=False):

        #harcoding this, we need to get this from master
        dataflow.map_id_op={}

        # dataflow.map_id_op['master']        ='172.17.15.21'
        # dataflow.map_id_op['task1_data']    ='127.0.0.1'
        # dataflow.map_id_op['task2_data']    ='127.0.0.1'

        # We need to decide an appropriate place to put it
        dataflow.soc_hel = socketHeliot()
        
        try:
            with open('mapping.json', 'r') as file:
                mapping = json.load(file)
        except Exception as e:
            dataflow.logs_file = open('dataflow.log', "w")
            dataflow.logs_file.write(str(e) + '\n')


        if get:
            dataflow.logs_file = open('dataflow_get_'+str(id)+'.log', "w")
            dataflow.map_id_op[id] = mapping[id]['in_port']

        else:
            dataflow.logs_file = open('dataflow_send_'+str(id)+'.log', "w")
            dataflow.map_id_op[id] = []
            for key, value in mapping.items():
                if 'out_devices' in value and id in value['out_devices']:
                    index = 0
                    for device in value['out_devices'][id]:
                        dataflow.map_id_op[id].append({
                            'ip':   mapping[device]['ip'],
                            'port': value['out_ports'][id][index]
                        })
                        index += 1
            dataflow.logs_file.write(str(dataflow.map_id_op))
            dataflow.logs_file.write('\n')
            dataflow.logs_file.flush()
                    
        
        
        #get the pid of the task and send it to the master using socket API



    # We need to send data with id
    @staticmethod
    def sendData(id, data):
        ip = port = None
        retry=1
        success = False
        while retry>0:
            try:
                if dataflow.map_id_op==None:
                    dataflow.set_data_input_mapping(id)

                for task in dataflow.map_id_op[id]:
                    ip      = task['ip']
                    port    = task['port']

                    #maintaing logs on storage
                    dataflow.logs_file.write('Sending data to: '+str(ip)+':'+str(port)+' at time:'+str(time.time()))
                    dataflow.logs_file.write('\n')
                    dataflow.logs_file.flush()
                    dataflow.soc_hel.sendData(ip,data,port)

                    #we don't need to retry now
                    retry = 0
                    success = True

            except Exception as e:
                dataflow.logs_file.write('error on ip: '+str(ip)+':'+str(port)+' at time:'+str(time.time()))
                dataflow.logs_file.write('\n')
                dataflow.logs_file.write('Exception: '+str(e))
                dataflow.logs_file.write('\n')
                dataflow.logs_file.write('Retry: '+str(retry))
                dataflow.logs_file.write('\n')
                dataflow.logs_file.flush()

                #we will retry again
                retry=retry-1
                success = False

        return success


    @staticmethod
    def getData(id):
        inport = None
        try:
            if dataflow.map_id_op==None:
                dataflow.set_data_input_mapping(id, True)

            #maintaing logs on storage
            dataflow.logs_file.write('getData: at time:'+str(time.time()))
            dataflow.logs_file.write('\n')
            dataflow.logs_file.flush()

            inport = dataflow.map_id_op[id]
            data=dataflow.soc_hel.getData(inport)
            return data

        except Exception as e:
            dataflow.logs_file.write('Error on: getData: at time:'+str(time.time()))
            dataflow.logs_file.write('\n')
            dataflow.logs_file.write(str(e))
            dataflow.logs_file.write('\n')
            dataflow.logs_file.write(str(inport))
            dataflow.logs_file.write('\n')
            dataflow.logs_file.flush()
            return None

# Send the data
