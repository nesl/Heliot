import socket
import pickle
import time
import sys

ids     = ['node1', 'node2']
ips     = ['10.0.0.101', '10.0.0.102']
ports   = [65000, 65000]
num     = 5
pic     = 'track.jpg'


class Node:
    log = None

    def __init__(self, id):
        self.id = id
        idx = ids.index(id)
        self.ip = ips[idx]
        self.port = ports[idx]
        self.log = open('dataflow_' + id + '.log', "w")


    def sendPic(self, recv):
        self.log.write('Sending data to ' + recv + ' at time:' + str(time.time()))
        self.log.write('\n')
        self.log.flush()

        idx = ids.index(recv)
        ip = ips[idx]
        port = ports[idx]

        client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Trying to connect to:', ip, ' on port:', port)
        client_socket.connect((ip, port))
        print ('Connected to %s on port %s' % (ip, port))
        self.log.write('Connected to %s on port %s' % (ip, port))


        file = open(pic,'rb')
        data = file.read(1024)
        while data:
            client_socket.send(data)
            data = file.read(1024)
        
        self.log.write('Done sending!')

        file.close()
        client_socket.close()


    def receivePic(self):
        self.log.write('Listening for data on ' + self.id + ' at time:' + str(time.time()))
        self.log.write('\n')
        self.log.flush()
        
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
        server_socket.bind((self.ip, self.port))          
        server_socket.listen() 
        print ("Listening...")                  
        
        conn, addr = server_socket.accept()
        print('Got connection from ' + str(addr))
        self.log.write('Got connection from ' + str(addr))
    
        with open('track_' + self.id + '.jpg', 'wb') as file:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                file.write(data)

        self.log.write('Received!')

        file.close()
        server_socket.close()



if __name__ == "__main__":
    if len(sys.argv) > 4 or len(sys.argv) < 3:
        print('usage: python3 sendPic.py <send, receive> <sender> receiver')
        print('Example: python3 sendPic.py send node1 node2')
        print('Example: python3 sendPic.py receive node2')
        exit(0)
        
    cmd         = str(sys.argv[1])
    
    if cmd == 'send':
        sender      = str(sys.argv[2])
        receiver    = str(sys.argv[3])
        send_node = Node(sender)
        send_node.sendPic(receiver)
        

    elif cmd == 'receive':
        receiver = str(sys.argv[2])
        receive_node = Node(receiver)
        receive_node.receivePic()

