from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import sys
import thread

from flask import Flask
import msgpackrpc

from tasklib.entity.base_server import BaseServer
from tasklib.utils.common_utils import update_rootlogger


update_rootlogger('webserver', is_log_to_file=True)
log = logging.getLogger()

g_CURRENT_RESULT = 'NULL'
g_CURRENT_CNT = 0


class RPCServer(object):
    def push(self, data):
        log.info('got data, size={}'.format(len(data)))
        global g_CURRENT_RESULT, g_CURRENT_CNT
        g_CURRENT_RESULT = data
        g_CURRENT_CNT += 1
        ret = 'receive data, cnt={}'.format(g_CURRENT_CNT)
        log.info(ret)
        return ret


app = Flask(__name__)


@app.route("/")
def main():
    global g_CURRENT_RESULT
    return g_CURRENT_RESULT


def flaskThread(web_ip, web_port):
    app.run(host=web_ip, port=int(web_port))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            'usage: python {0} WEB_IP:WEB_PORT RPC_IP:RPC_PORT. \n'
            'e.g. python {0} 172.17.51.1:7788 172.17.51.1:18900'.format(
                sys.argv[0]))
        exit(0)
    print('{} running at {} and getting data from {}'.format(
        sys.argv[0], sys.argv[1], sys.argv[2]))
    web_ip, web_port = sys.argv[1].split(':')
    rpc_ip, rpc_port = sys.argv[2].split(':')

    thread.start_new_thread(flaskThread, (web_ip, web_port,))

    # rpc server
    server = BaseServer('webserver', RPCServer())
    server.listen(msgpackrpc.Address(rpc_ip, int(rpc_port)))
    server.start()
