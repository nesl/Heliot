import sys

sys.path.append('../../')


from testbed import *

def get_connection(ip='', username='', password=''):
    con = connection('_ssh')
    con.add_attribute('_ip',ip)
    con.add_attribute('_username',username)
    con.add_attribute('_password',password)
    return con

def get_testbed():

    #mininet_server
    mininet_server = device(id='device_mininet',type='_mininet_server')
    mininet_server.add_os(osHeliot('_ubuntu'))
    mininet_server.add_connection(get_connection('172.17.15.21','xx', 'xx'))

    #airsim_server
    airsim_server = device(id='device_airsim',type='_airsim_server')
    airsim_server.add_os(osHeliot('_windows'))
    airsim_server.add_connection(get_connection('172.17.49.168','xx', 'xx'))

    #Tx2
    nvidia_jetson_tx2 = device(id='device_tx2',type='_nvidia_jetson_tx2')
    nvidia_jetson_tx2.add_os(osHeliot('_ubuntu'))
    nvidia_jetson_tx2.add_connection(get_connection('172.17.49.60','xx', 'xx'))

    #gvk
    google_vision_kit = device(id='device_gvk',type='_google_vision_kit')
    google_vision_kit.add_os(osHeliot('_ubuntu'))
    google_vision_kit.add_connection(get_connection('172.17.15.21','root', 'pwd'))

    android_smartphone = device(id='device_phone',type='_smartphone')
    android_smartphone.add_os(osHeliot('android'))
    ## Require a special kind of REST API connection.


    my_testbed = testbed(name='my_demo_testbed')
    # Takes any user defined name as input, can be left empty

    # Adding devices
    my_testbed.add_device(mininet_server)
    my_testbed.add_device(airsim_server)
    my_testbed.add_device(nvidia_jetson_tx2)
    my_testbed.add_device(google_vision_kit)
    my_testbed.add_device(android_smartphone)

    return my_testbed
