"""
The definition of workload in Heliot consists of Testbed and Scenario

Testbed defines the physical devices. The devices are defined in core folder.
Testbed consists of list of devices

"""

"""
Logic and predefined heliot keywords used in the testbed file:

1) device should have unique id. A list of id is maintained and it is ensured each device has unique id
2) Predefined keywords for connection object in device is used to validate the existence of testbed
Keywords: _ssh (_ip)

"""


#Heliot imports
from core.device import *
from utils.ping import *

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



class testbed:

# testbed has list of devices
# device attributes  defines the device in more details
# device attributes are: list of compute, memory, list of connection, list of sensors, os and description



    def __init__(self,name=''):
        self._name = name

        # _device store the list of physical devices
        self._device = []

        # Stores the ids of all the devices in the testbed
        # all devices should have unique ids
        self._id = []

    # Add device to the list of devices in the testbed
    def add_device(self, d):
        #verify c is compute object
        if type(d) is device:
            id = d._id
            print('Adding device ',id, ' to testbed')
            # check if device of this id is already present in testbed
            if str(id) in self._id:
                logger.error(str(id)+' is already present in testbed')
                logger.error('id of each device should be unique')
                sys.exit()

            self._device.append(d)
            self._id.append(str(id))

        else:
            logger.error('add_device called with wrong input')
            sys.exit()

    # get the list of devices in the current testbed
    def get_device(self):
        return self._device

    def get_info(self):
        return self._name, self._device


# Validation is very important step of testbed in heliot
# We need to ensure all the devices are reachable by heliot_runtime
# Steps:
# 1) We first do ping in case of linux/windows devices. For Android, we try to communicate to the Andoid app running rest api


    def validate(self):

        logger.info('Validating the devices in Testbed')

        #Validate each device in the testbed
        for dev in self._device:

######################################Checking connectivity of all devices first #######################################################
            #In case no connection object is present
            if len(dev.get_connection())==0:
                logger.error(str(con._type) +' is not known to heliot')
                logger.error(str(dev._id) +'  cannot be reached')
                logger.error('Testbed validation failed')
                sys.exit()

            #connection object of device
            con = dev.get_connection()[0] #At present, there is only one type of connection obect which is ssh/restAPI


            if con._type =='_ssh':
                ip = con._attributes['_ip']
                val = check_ping(address=ip)
                if not val:
                    logger.error(str(dev._id) +'  cannot be reached')
                    logger.error('Testbed validation failed')
                    sys.exit()

                logger.info(str(dev._id)+' is connected')

                # After ping, now doing ssh connection and downloading heliot github repo on devices
                




            else :
                logger.error(str(con._type) +' is not known to heliot')
                logger.error(str(dev._id) +'  validation failed')
                logger.error('Testbed validation failed')
                sys.exit()

        logger.info('Testbed validated')

#t1 = testbed('mytestbed')

#print(t1.get_info())
