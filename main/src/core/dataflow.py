'''
Provides dataflow functionality to the heliot tasks
Different tasks can communicate with each other using input and output datastructures

The functionality of the class is explained as below:

'''

import msgpackrpc

class dataflow(object):

    def __init__(self):
        self._data = {}
        self.ids=['id_1','id_2']
        self.ids2=[]

    def receive(self, data_id, data):
        if isinstance(data_id,str):
            self._data[data_id]=data
            self.ids2.append(data_id)
            #check if all the expected data ids have arrived and proceed to execute the task

            ## Maybe fork a thread  to do this parallel and see the performance

            ## check for all the expected data ids
            if self.ids.sort() == self.ids2.sort():


            ## Execute the task
            print('Executing the task')
            ## Push the output of the task to other devices



            return True


        return False




# Used for local testing
server = msgpackrpc.Server(dataflow())
server.listen(msgpackrpc.Address("localhost", 18800))
server.start()
