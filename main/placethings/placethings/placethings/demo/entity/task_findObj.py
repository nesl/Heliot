from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import base64
import logging
import io
import subprocess
import time

from PIL import Image

from placethings.demo.entity import task as BaseTask
from placethings.demo.entity.base_client import ClientGen


log = logging.getLogger()


class RPCServer(BaseTask.RPCServer):
    def __init__(
            self, name, exec_delay_time_ms, receiver_list=None,
            extra_param_list=None):
        super(RPCServer, self).__init__(
            name, exec_delay_time_ms, receiver_list, extra_param_list)
        self._imgid = 0
        log.info('Class Flavor: task_findObj')

    def _compute(self, data, extra_param_list):
        t1 = time.time()
        log.info('(TIME) start computation: {}'.format(t1))
        log.info('finding object')
        mode = extra_param_list[0]
        if mode == 'offload':
            next_ip, next_port = extra_param_list[1].split(':')
            next_port = int(next_port)
            log.info('push data to {}:{}'.format(next_ip, next_port))
            result = ClientGen.call(next_ip, next_port, 'push', data)
        else:
            yolo_folder = '/opt/github/darknet'
            image_data = base64.b64decode(data)
            image = Image.open(io.BytesIO(image_data))
            img_name = 'img_{}.png'.format(self._imgid)
            self._imgid += 1
            image.save('{}/{}'.format(yolo_folder, img_name), 'PNG')
            cmd = (
                './darknet detect cfg/yolov3-tiny.cfg '
                'yolov3-tiny.weights {}').format(img_name),
            proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, shell=True, cwd=yolo_folder,)
            result = proc.communicate()[0]
            if self.exec_delay_time_sec > 0:
                time.sleep(self.exec_delay_time_sec)
            t2 = time.time()
        if self.exec_delay_time_sec > 0:
            time.sleep(self.exec_delay_time_sec)
        t2 = time.time()
        # logging
        log.info('compute result: {}'.format(result))

        log.info('(TIME) stop computation: {}'.format(t2))
        log.info('computation result:\n{}'.format(result))
        return 'exec_time: {}, result:\n{}'.format(t2-t1, result)
