import socket
import pickle
import time
import sys
import json

log = open('dataflow_t2.log', "w")

def sendData(id, ip, port):
    log.write('Listening for data on ' + id + ' at time:' + str(time.time()))
    log.write('\n')
    log.flush()
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
    server_socket.bind((ip, port))          
    server_socket.listen() 
    print ("Listening... on ip:", ip, "port:", port)                  
    
    conn, addr = server_socket.accept()
    print('Got connection from ' + str(addr))
    log.write('Got connection from ' + str(addr))

    with open('data_' + id + '.txt', 'wb') as file:
        while True:
            data = conn.recv(25)
            if not data:
                break
            file.write(data)

    log.write('Received!')

    file.close()
    server_socket.close()



if __name__ == "__main__":
    print('t2 receiving')

    with open('map.json', 'r') as file:
        map = json.load(file)

    port = map['t2']['in_port']
    ip = ''#map[ map['t2']['device'] ]['ip']

    sendData('t2', ip, port)