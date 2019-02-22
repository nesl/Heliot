'''
# This is a skeleton of the task

Provides task functionality to the heliot scenario

The functionality of the class is explained as below:
'''

#other imports
import sys
import logging



logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
ch.setLevel(logging.DEBUG)

logger.addHandler(ch)

logger.setLevel(logging.DEBUG)

class taskHeliot(object):

    # 3 _type of tasks: _compute, _virtualSensing, _alertAndroid
    #  _taskid is used to uniquely identify the tasks
    # _filename, the file used to run the task
    # _nodeid, this may be given or left empty. This tell where to schedule the task
    ## if this is empty, it triggers Heliot computation to do automatic placement

    def __init__(self,_type='',_taskid='',_file='', _nodeid=''):
        self._type = _type

        self._taskid = _taskid
        self._file = _file
        self._nodeid = _nodeid
        self._outputids =[]
        self._inputids=[]

    def get_output(self,_outputid=''):
        if isinstance(_outputid, str):
            if _outputid in self._outputids:
                # Note this id is already part of task output and
                # We give warning and igore it.
                logger.warning('get_output '+ _outputid +' is already present')
                return _output_id

            self._outputids.append(_outputid)
            print(_outputid, ": is set as output for task: ",self._taskid)
            #We need to define a class for data_ids, which may keep track of
            #many other statistics and functionalities
            return _outputid
        else:
            logger.error('get_output called with wrong input')
            sys.exit()

    def set_input(self,_inputids=[]):
        #ToDO: Note we need to verify the type of _inputids as well

        for id in _inputids:
            if id in self._inputids:
                logger.warning('set_input '+ id +' is already present')
            else:
                self._inputids.append(id)
                print(id, ": is set as input for task:",self._taskid)
