'''
Provides dataflow functionality to the heliot tasks
Different tasks can communicate with each other using input and output datastructures

The functionality of the class is explained as below:
Pickle is used to send data using Sockets
'''

import socket
import numpy as np
import pickle

class socketHelot:
    def __init__(self):
        self.port=7555
        pass

    #Opens a socket and listens for data
    def receiveData(self):

        server_socket=socket.socket()
        server_socket.bind(('',self.port))
        server_socket.listen(1)
        print('waiting for a connection...')

        client_connection,client_address=server_socket.accept()
        print('connected to ',client_address[0])

        ultimate_buffer=None

        while True:
            data = client_connection.recv(1024)
            if not data:
                break
            if ultimate_buffer==None:
                ultimate_buffer=data
            else:
                ultimate_buffer= ultimate_buffer+data

        #print(ultimate_buffer)
        client_connection.close()
        server_socket.close()
        ultimate_buffer = pickle.loads(ultimate_buffer)
        #print(ultimate_buffer)
        #print('\n Data received')
        return ultimate_buffer

    # uses socket to send the data
    def sendData(self, server_address,Data):
        client_socket=socket.socket()

        try:
            client_socket.connect((server_address, self.port))
            print ('Connected to %s on port %s' % (server_address, port))
        except Exception as e:
            print('Exception:',e)
            return False

        data_string = pickle.dumps(Data)
        #print(data_string)
        client_socket.sendall(data_string)
        client_socket.close()
        #print('numpy data sent')
        return True
