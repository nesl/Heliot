# Create a dataflow for the demo

from .dataflow import *

#receiving ports
recv = {}
recv['cam']=20000 #internal port of docker listening on the machine 19000
recv['tx2']=20000
recv['android']=20000

#Send ip and ports
send = {}
send['cam']    = '10.0.0.102'  #sending to tx2 container over port 20000 (internal port)
send['tx2']    = '172.17.49.71' #sending to tx2 machine
send['android']='172.17.15.21' #sending to android server


if __name__ == "__main__":

	# #There is input port argument
	if len(sys.argv)!=2:
		print('usage: python3 mininetDemo.py container')
		print('Example: python3 mininetDemo.py cam')
		exit(0)

	#Parsing the input argument
	type=int(sys.argv[1])

    #listen on a socket and start the server to receive data
    while true:
        data = dataflow.getData()
