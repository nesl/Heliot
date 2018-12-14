from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import importlib
import logging
import msgpackrpc
import time

from tasklib.entity.base_client import BaseClient
from tasklib.entity.task import RPCServer as TaskRPCServer


log = logging.getLogger()


class BaseServer(msgpackrpc.Server):
    def __init__(self, name, dispatcher):
        self.name = name
        super(BaseServer, self).__init__(dispatcher)

    @staticmethod
    def _obj_to_str(obj):
        obj_str = str(obj)
        limit_len = min(64, len(obj_str))
        return obj_str[:limit_len]

    def dispatch(self, method, param, responder):
        # get timestamp
        t2 = time.time()
        t1 = param.pop()
        # t1 = param.pop()
        log.info('====== receive pkt ======')
        log.info('(TIME) pkt sent time: {}'.format(t1))
        log.info('(TIME) pkt rcev time: {}'.format(t2))
        log.info('(TIME) transmit time: {}'.format(t2 - t1))
        log.info('(RECV) {}: {}'.format(method, self._obj_to_str(param)))
        # dispatch
        method = msgpackrpc.compat.force_str(method)
        if method == 'STOP':
            log.info('stop server: {}'.format(self.name))
            result = True
            if isinstance(result, msgpackrpc.server.AsyncResult):
                result.set_responder(responder)
            else:
                responder.set_result(result)
            self.stop()
            self.close()
        else:
            super(BaseServer, self).dispatch(method, param, responder)


class ServerGen(object):

    _RPC_CLS = {
        "task": TaskRPCServer,
    }

    @classmethod
    def start_server(
            cls, name, entity_name, ip, port, *args):
        args = [name] + list(args)
        log.info('start_server {} at {}:{}'.format(name, ip, port))
        log.info('args={}'.format(args))
        if entity_name in cls._RPC_CLS:
            entity_class = cls._RPC_CLS[entity_name]
            log.info('try to start base entity {}'.format(entity_name))
        else:
            module_name = 'tasklib.entity.{}'.format(entity_name)
            log.info('run rpc_server from {}'.format(module_name))
            entity_module = importlib.import_module(module_name)
            entity_class = getattr(entity_module, 'RPCServer')
        rpcobj = entity_class(*args)
        server = BaseServer(name, rpcobj)
        server.listen(msgpackrpc.Address(ip, port))
        server.start()

    @staticmethod
    def stop_server(ip, port):
        client = BaseClient('ServerGen', ip, port)
        result = client.call('STOP')
        log.info('stop server at {}:{}, {}'.format(ip, port, result))
