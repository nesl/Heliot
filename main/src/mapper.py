from core.device import *
from core.taskHeliot import *
import sys
import json


# Logger
import logging
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)


class mapper:

    initialOutPort  = 7000
    initialInPort   = 8000


    def __init__(self):
        self.map = {}


    @staticmethod
    def getOutPort():
        outport = mapper.initialOutPort
        mapper.initialOutPort += 1
        return outport

    @staticmethod
    def getInPort():
        inport = mapper.initialInPort
        mapper.initialInPort += 1
        return inport

    
    def addTaskMapping(self, _task, _device):
        if self.checkTask(_task) and self.checkDevice(_device):
            inPort = None
            outPorts = {}
            dev = _device._id
            out_devices = {}

            for output in _task._outputids:
                outPorts[output] = []
                out_devices[output] = []

            if len(_task._inputids) != 0:
                inPort = mapper.getInPort()
                
            self.map[_task._taskid] = {
                'in_port': inPort,
                'out_ports': outPorts,
                'device': dev,
                'out_devices': out_devices
            }


    def addMasterMapping(self, _device):
        if self.checkDevice(_device):
            pass


    def addDeviceMapping(self, _device):
        if self.checkDevice(_device):
            self.map[_device._id] = { 'ip': _device.get_connection()[0]._attributes['_ip'] }


    def mapDataflow(self, tasks, devices, nodes, dir):
        print(self.map)
        for task in tasks:
            for input_id in task._inputids:
                for key, value in self.map.items():
                    if 'out_ports' in value and input_id in value['out_ports']:
                        self.map[key]['out_ports'][input_id].append(self.map[task._taskid]['in_port'])
                        self.mapOutDevice(key, input_id, task, devices, nodes)
        
        with open(dir, 'w') as file:
            json.dump(self.map, file, sort_keys=True, indent=4)     
    

    def mapOutDevice(self, key, input_id, task, devices, nodes):
        for node in nodes:
            if node._id == task._nodeid:
                for device in devices:
                    if device._type == node._type:
                        self.map[key]['out_devices'][input_id].append(device._id)
                              
                
    def checkTask(self, _task):
        if type(_task) is taskHeliot:
            return True
        else:
            logger.error("Task mapping must have an argument of type task")
            sys.exit()

    def checkDevice(self, _device):
        if type(_device) is device:
            return True
        else:
            logger.error("Device mapping must have an argument of type device")
            sys.exit()


"""
map = {
    'task_1': { 
        'in_port': #, 
        'out_ports': { 'task1_data': [#, ...], ... }, 
        'device': 'device_x',
        'out_devices: { 'task1_data': ['device_x', ...], ... }
    },
    'task_2': ...,
    ...,
    'master': 'device_x',
    'device_x': { ip: },
    ...,
}
"""


"""
BEFORE
{ 
   'prince_device':{ 
      'ip':'127.0.0.1'
   },
   'task3':{ 
      'in_ports':8000,
      'out_ports':{ 

      },
      'device':'prince_device',
      'out_devices':{ 

      }
   },
   'task4':{ 
      'in_ports':8001,
      'out_ports':{ 

      },
      'device':'prince_device',
      'out_devices':{ 

      }
   },
   'task1':{ 
      'in_ports':None,
      'out_ports':{ 
         'task1_data':[ 

         ]
      },
      'device':'prince_device',
      'out_devices':{ 
         'task1_data':[ 

         ]
      }
   },
   'task2':{ 
      'in_ports':None,
      'out_ports':{ 
         'task2_data':[ 

         ]
      },
      'device':'prince_device',
      'out_devices':{ 
         'task2_data':[ 

         ]
      }
   }
}
"""


"""
AFTER
{ 
   'prince_device':{ 
      'ip':'127.0.0.1'
   },
   'task3':{ 
      'in_ports':8000,
      'out_ports':{ 

      },
      'device':'prince_device',
      'out_devices':{ 

      }
   },
   'task4':{ 
      'in_ports':8001,
      'out_ports':{ 

      },
      'device':'prince_device',
      'out_devices':{ 

      }
   },
   'task1':{ 
      'in_ports':None,
      'out_ports':{ 
         'task1_data':[ 
            8000,
            8001
         ]
      },
      'device':'prince_device',
      'out_devices':{ 
         'task1_data':[ 
            'prince_device',
            'prince_device'
         ]
      }
   },
   'task2':{ 
      'in_ports':None,
      'out_ports':{ 
         'task2_data':[ 
            8000,
            8001
         ]
      },
      'device':'prince_device',
      'out_devices':{ 
         'task2_data':[ 
            'prince_device',
            'prince_device'
         ]
      }
   }
}
"""
