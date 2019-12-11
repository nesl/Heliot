import socket
import pickle
import time
import sys
import json

dataFile = 'data.txt'
log = open('dataflow_t1.log', "w")

def sendData(recv, ip, port):
    log.write('Sending data to ' + recv + ' at time:' + str(time.time()))
    log.write('\n')
    log.flush()

    # idx = ids.index(recv)
    # ip = ips[idx]
    # port = ports[idx]

    client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Trying to connect to:', ip, ' on port:', port)
    client_socket.connect((ip, port))
    print ('Connected to %s on port %s' % (ip, port))
    log.write('Connected to %s on port %s' % (ip, port))


    file = open(dataFile,'rb')
    data = file.read(25)
    while data:
        client_socket.send(data)
        data = file.read(25)
    
    log.write('Done sending!')

    file.close()
    client_socket.close()



if __name__ == "__main__":
    print('t1 sending to t2')

    with open('map.json', 'r') as file:
        map = json.load(file)

    # deviceToSendName = map['t1']['out_devices']['t1_data'][0]
    port = map[ map['t1']['node'] ]['port']
    ip = map[ map['t1']['node'] ]['ip']

    sendData('t2', ip, port)
