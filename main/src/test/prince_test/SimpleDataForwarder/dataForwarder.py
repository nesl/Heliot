import socket
import pickle
import time
import sys
import json


class Node:
    log = None

    def __init__(self, id, in_ip, in_port, out_ip, out_port):
        self.id = id
        self.in_ip = in_ip
        self.in_port = in_port
        self.out_ip = out_ip
        self.out_port = out_port
        self.log = open('dataflow_node_' + id + '.log', "w")


    def forward(self):

        # Receive Data
        self.log.write('Listening for data on ' + self.id + ' at time:' + str(time.time()))
        self.log.write('\n')
        self.log.flush()
        
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
        server_socket.bind((self.in_ip, self.in_port))          
        server_socket.listen() 
        print ("Listening...")                  
        
        conn, addr = server_socket.accept()
        print('Got connection from ' + str(addr))
        self.log.write('Got connection from ' + str(addr))
    
        while True:
            data = conn.recv(25)
            if not data:
                break

            self.log.write('Received: ' + str(data))
            
            # Send Data
            self.log.write('Sending data at time:' + str(time.time()))
            self.log.write('\n')
            self.log.flush()

            client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print('Trying to connect to:', self.out_ip, ' on port:', self.out_port)
            client_socket.connect((self.out_ip, self.out_port))
            print ('Connected to %s on port %s' % (self.out_ip, self.out_port))
            self.log.write('Connected to %s on port %s' % (self.out_ip, self.out_port))

            while data:
                client_socket.send(data)
            
            self.log.write('Done sending: ' + str(data))

        server_socket.close()
        client_socket.close()



if __name__ == "__main__":
    if len(sys.argv) > 4 or len(sys.argv) < 3:
        print('usage: python3 dataForwarder.py <send, receive> <sendtask> <receiveTask>')
        print('Example: python3 dataForwarder.py send t1 t2')
        print('Example: python3 dataForwarder.py receive t2')
        exit(0)
        
    cmd = str(sys.argv[1])
    with open('map.json', 'r') as file:
        map = json.load(file)
    
    if cmd == 'send':
        sender      = str(sys.argv[2])
        receiver    = str(sys.argv[3])
        node        = map[sender]['node']
        in_ip       = map[node]['ip']
        in_port     = map[node]['port']
        out_ip      = map[ map[receiver]['node'] ]['ip']
        out_port    = map[ map[receiver]['node'] ]['port']

        send_node   = Node(node, in_ip, in_port, out_ip, out_port)
        send_node.forward()
        

    elif cmd == 'receive':
        receiver        = str(sys.argv[2])
        node            = map[receiver]['node']
        in_ip           = map[node]['ip']
        in_port         = map[node]['port']
        out_ip          = map[ map[receiver]['device'] ]['ip']
        out_port        = map[receiver]['in_port']

        receive_node    = Node(node, in_ip, in_port, out_ip, out_port)
        receive_node.forward()

