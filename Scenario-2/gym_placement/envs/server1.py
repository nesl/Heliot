"""
Server task file
"""

#Receives data from the edge

import numpy as np
from socketHeliot import *
import time

#Repeat = 10000
#edge ip
ip = '10.0.0.21' #'localhost'

Data = np.identity(10) #identity matrix
data_string_server = pickle.dumps(Data, protocol=3)

soc_hel = socketHeliot()

#sendData(ip,data,inport)
print("receiving data")

while(True):
    #t_start = time.time()
    data_string = soc_hel.getData()

    if data_string!=None:
        soc_hel.sendData(ip,data_string_server,inport=7556)
    #t_done  =  time.time()

    #print('Data received is:',data.shape)
    #print(t_start,t_done, t_done-t_start)
    #print(t_recv_done)
