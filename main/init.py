
# Starting init process on each device which communicates
# to the the coordinator

import msgpackrpc

Heliot_Client_Port=18800

class Heliot_Client(object):

    ## Coordinator calls check_connection
    ## and devices return true if they are working
    def check_connection(self):
        return True

server = msgpackrpc.Server(Heliot_Client())
server.listen(msgpackrpc.Address("localhost", Heliot_Client_Port))
server.start()
