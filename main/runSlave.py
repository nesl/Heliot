
#Making one module visible to another
import sys
sys.path.append('../')

from rpc.SlaveRpc import SlaveRpc
from rpyc.utils.server import ThreadedServer


server = ThreadedServer(SlaveRpc, port=18861, protocol_config={
    'allow_public_attrs': True, "allow_all_attrs": True
})

server.start()
