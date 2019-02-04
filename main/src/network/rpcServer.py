# This file is used to make the dataflow between different tasks

# The logic is as below:
# 1. This class will provide a RPC server functionality
# 2. The RPC server will run using a threading in python in parallel to the task to be
# done on the node
# 3. Function: send_data: called by the local task. This is used to send data
# to the rpc server running on any other node
# Note: we have to make an exception where this send data is used for task alert on android
# In this case, the mininet code has to handle it intelligently by using the rest api interface other
# than the rpc interface

# 4. Function: get_data: This is called by both local task.
# When called: we need to get a data of a particular id, so this may result in the blocking of the queue
# if data is not available

# 5. Function: rec_data: This is called from the remote task
# We are passing data from remote task, so now the queue block is unset if all ids are available and
# any blocked task may proceed

import thread
import time

import msgpackrpc

from Queue import Queue
common_queue = Queue()

#local data for the task
def get_data():
    print 'get_data waiting'
    common_queue.put([])#putting empty request
    common_queue.join()
    print 'get_data done'

class rpcServer(object):
    def send_data(self, ip):
        print 'Send Data'
        try:
            client = msgpackrpc.Client(msgpackrpc.Address(ip, 4001))
            client.call('rec_data')
        except Exception as e:
            print 'send_data:',e


    def rec_data(self):
        print 'global received'
        #res = common_queue.get()

#simulate rpc server on local host
def thread1(name):
    print 'starting rpcServer: ',name
    server = msgpackrpc.Server(rpcServer())
    server.listen(msgpackrpc.Address("localhost", 4000))
    server.start()

# simulate rpc server on another host
def thread2(name):
    print 'starting rpcServer: ',name
    server = msgpackrpc.Server(rpcServer())
    server.listen(msgpackrpc.Address("localhost", 4001))
    server.start()


# simulate the data send from remote task
def thread3(name):
    print 'starting thread3',name
    time.sleep(2)

    client = msgpackrpc.Client(msgpackrpc.Address("localhost", 4000))
    while True:
        try:
            client.call('send_data', "127.0.0.1")
            time.sleep(5)
        except Exception as e:
            print 'thread3:',e

# simulate the data request from local host
def thread4(name):
    print 'starting thread4',name
    time.sleep(2)

    while True:
        try:
            get_data()
            time.sleep(2)
        except Exception as e:
            print 'thread4:',e


# def thread2(name):
#     print 'starting thread2',name
#     client = msgpackrpc.Client(msgpackrpc.Address("localhost", 4000))
#     while True:
#         res = client.call('rec_data', 0)
#         print 'res is:',res
#         time.sleep(2)


# simulate the remote data transfer


# Create two threads as follows
#Start rpcServer
thread.start_new_thread( thread3,("Thread-3",) )
thread.start_new_thread( thread2,("Thread-2",) )
#thread.start_new_thread( thread1,("Thread-1",) )


#local rec_data
#thread.start_new_thread( thread3,("Thread-3",) )

thread1("Thread-1")

# while 1:
#    pass
