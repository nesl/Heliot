'''
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

    def __init__(self,_taskid='',_filename='', _nodeid=''):
        self._filename = _filename
        self._taskid = _taskid
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

    def run_task(self):
        pass
        #Add logic to run_task
            #Import the taskfile
            #Call the run function