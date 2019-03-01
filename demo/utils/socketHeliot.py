'''
Provides dataflow functionality to the heliot tasks
Different tasks can communicate with each other using input and output datastructures

The functionality of the class is explained as below:
Pickle is used to send data using Sockets
'''

import socket
import numpy as np
import pickle

class socketHeliot:
    def __init__(self):
        self.port=7555
        pass

    #Opens a socket and listens for data
    def getData(self, inport=None):
        ultimate_buffer=None

        server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if inport==None:
            server_socket.bind(('',self.port))
        else:
            server_socket.bind(('',inport))

        server_socket.listen(1)
        print('waiting for a connection...')

        client_connection,client_address=server_socket.accept()
        print('connected to ',client_address[0])



        while True:
            data = client_connection.recv(1024)
            if not data:
                break
            if ultimate_buffer==None:
                ultimate_buffer=data
            else:
                ultimate_buffer= ultimate_buffer+data

        #print('ultimate_buffer is:',ultimate_buffer)
        client_connection.close()
        server_socket.close()

        if ultimate_buffer!=None:
            ultimate_buffer = pickle.loads(ultimate_buffer)
            #print(ultimate_buffer)
            #print('\n Data received')

        return ultimate_buffer

    # uses socket to send the data
    def sendData(self, server_address, Data, inport=None):
        client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #print('Trying to connect to:',server_address, ': on port:',self.port)

        if inport ==None:
            client_socket.connect((server_address, self.port))
        else:
            client_socket.connect((server_address, inport))
            
        #print ('Connected to %s on port %s' % (server_address, self.port))

        data_string = pickle.dumps(Data, protocol=3)
        #print(data_string)
        client_socket.sendall(data_string)
        client_socket.close()

        return True
