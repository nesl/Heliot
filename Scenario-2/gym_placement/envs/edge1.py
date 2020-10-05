"""
Edge task file
"""

#sends data to the server
import numpy as np
from socketHeliot import *
import time
import pickle
import sys
import random
import pprint

size = 100
ip = '10.0.0.22' #'localhost'
Repeat = 5
num_actions = 4 #Total different types of compute split, total compute parts are also 4. Total actions are 5 (0,1,2,3,4)
time_for_each_unit = 0.2 #time to each part of compute unit is uniformly selected to 0.2

Data = np.identity(size) #identity matrix
data_string = pickle.dumps(Data, protocol=3)

#action input to the edge task
action=int(sys.argv[1])
#print('Action is:',action)

"""
action = 0, everything local
action = 4, everything on the server
When more compute on edge, it will take more time to complete the compute
when more compute on server, data to transfer will be more
"""

local_time = (num_actions - action)*time_for_each_unit
data_string_send = data_string*action

total_time = 0.0

experience=None

if action==0:
    total_time = local_time

    experience=[action,total_time]

if action!=0: #we have to send some data to the server
    #print("Size of data_string:",sys.getsizeof(data_string))
    soc_hel = socketHeliot()
    t_start = time.time()
    soc_hel.sendData(ip,data_string_send)#sendData(ip,data,inport)
    data_recv = soc_hel.getData(inport=7556)
    t_done  =  time.time()

    if data_recv!=None:
        total_time = local_time+(t_done-t_start)
        experience=[action,total_time]

    else:
        print('Failed :',i)

#print("Experience is:",experience)
#print('Save the experience data collected')
pickle.dump( experience, open( "experience.p", "wb" ), protocol=2)
