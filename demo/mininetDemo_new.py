# Create a dataflow for the demo

from utils.dataflow import *
import sys
from flask import Flask

#internal port of docker listening on the machine 19000

# #receiving ports
# recv = {} #these are external ports of docker
# recv['cam']=20000
# recv['tx2']=20001
# recv['act']=20002
#
# #Send ip and ports
# send = {}
# send['cam']    = '10.0.0.102'   #  sending to tx2 container over port 19000 (internal port)
# send['tx21']    = '172.17.49.71'#  sending to tx2 machine over port 19000
# send['tx22']    = '10.0.0.103'  #  sending to act container over port 19005, different port
# send['act']    = '172.17.15.21' #  sending to android server over port 19000

#starting tasks on individual containers
# cd /opt/github/placethings/Heliot/demo && python3 mininetDemo_new.py 'cam'
#cd /opt/github/placethings/Heliot/demo && python3 mininetDemo_new.py 'tx2'

if __name__ == "__main__":
	if len(sys.argv)!=2:
		print('usage: python3 mininetDemo.py container')
		print('Example: python3 mininetDemo.py cam')
		exit(0)

	#Parsing the input argument
	type=str(sys.argv[1])


	#keeping track of number of data items received at each container
	data_index = 1

	#this is camera container
	if type == 'cam':
		print('Starting cam container')
		#receive images on port 20000 and forward them to tx2 container on 10.0.0.102
		while True:
			data = dataflow.getData(inport=20000)
			res = False
			if data!=None:
				print('cam received image:', data_index)
				data_index = data_index + 1
				res = dataflow.sendData('tx2_container_data',data) #Send image to cam container
			print('res is:',res)

	#This is the tx2 container
	if type =='tx2':
		print('starting tx2 container')
		#Tx2 container receives data from cam container
		#tx2 container sends data to the tx2 machine

		while True:
			data = dataflow.getData(inport=10001) #get the image from cam container
			res=False
			if data!=None:
				data_index = data_index + 1
				res = dataflow.sendData('tx2_machine_inference',data)#sending the image to the the tx2 physical machine
				#print('sending tx2 machine res is:',res)
				print('tx2 conainter received image:', data_index,' : ', res)

				#receive the labels from tx2 machine only if we send data
				if res:
					labels = dataflow.getData(inport=20001) #get the labels
					#print('labels are:',labels)


					if labels!=None:
						#send labels to the actuator container
						res = dataflow.sendData('act_container',labels)
						print('sending act_container res is:',res)


	#This is the actuation container
	if type =='act':
		print('starting act container')

		while True:
			labels = dataflow.getData(inport=10002) #get the labels from the tx2 container

			if labels!=None:
				data_index = data_index + 1
				res = dataflow.sendData('act_task',labels)#sending labels to the actuation task which can host it
				#print('sending android res is:',res)
				print('act received lables:',data_index,' : send res: ',res)