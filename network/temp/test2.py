import thread
import time

import msgpackrpc

class SumServer(object):
    def sum(self, x, y):
        return x + y

def thread1(name):
    print 'starting thread1: ',name
    server = msgpackrpc.Server(SumServer())
    server.listen(msgpackrpc.Address("localhost", 4000))
    server.start()

def thread2(name):
    print 'starting thread2',name
    client = msgpackrpc.Client(msgpackrpc.Address("localhost", 4000))
    while True:
        res = client.call('sum', 1, 2)
        print 'res is:',res
        time.sleep(5)


# Create two threads as follows
thread.start_new_thread( thread1,("Thread-1",) )
thread.start_new_thread( thread2,("Thread-2",) )

while 1:
   pass
