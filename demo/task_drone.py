import airsim

import numpy as np
import os
import tempfile
import pprint
import sys

import msgpackrpc
import time
import base64
import threading
from msgpackrpc.error import RPCError

from utils.dataflow import *

#C:\Users\Heliot Nesl\Desktop\Demo\images

image_folder = 'C:\\Users\\Heliot Nesl\\Desktop\\Demo\\images'
image_id = {
    'Drone1': 1,
}

#Scenario's are 4 here for the conix demo
Scenario = 1 # no rain no dust on the route: move_drone('Drone1', 35, 10, -1.5, 90, 2.5),  move_drone('Drone1', 10, 10, -1.5, 90, 2.5)
#Scenario = 2 # rain and dust enabled on the route: move_drone('Drone1', 35, 10, -1.5, 90, 2.5),  move_drone('Drone1', 10, 10, -1.5, 90, 2.5)

#Scenario = 3 # no rain and no dust enabled on the route: move_drone('Drone1', 100, 0, -2, 90, 2.5),  move_drone('Drone1', 10, 10, -1.5, 90, 2.5)
#Scenario = 3 # rain and dust enabled on the route: move_drone('Drone1', 10, 0, -2, 90, 2.5),  move_drone('Drone1', 10, 10, -1.5, 90, 2.5)


#get which scenario is running
def get_scenario():
    global Scenario

    while True:

        try:
            data = dataflow.getData(inport=10009) #get the scenario from any machine on the network, scenario port is: 10009
            if data!=None:
                Scenario = data

                if Scenario==0:
                    break #exit from the loop when scenaio is 0

                print('scenario is:',data)
                if Scenario == 1 or Scenario ==3:
                    client.simSetWeatherParameter(airsim.WeatherParameter.Rain, 0.0);
                    client.simSetWeatherParameter(airsim.WeatherParameter.Dust, 0.0);
                elif Scenario == 2 or Scenario ==4 :
                    client.simSetWeatherParameter(airsim.WeatherParameter.Rain, 0.45);
                    client.simSetWeatherParameter(airsim.WeatherParameter.Dust, 0.25);
        except Exception as e:
            pass


def take_picture(drone_name, is_save=False):
    responses = client.simGetImages([airsim.ImageRequest("front_center", airsim.ImageType.Scene)], vehicle_name=drone_name)

    if is_save:
        drone_image_folder = '{}\\{}'.format(image_folder, drone_name)
        if not os.path.isdir(drone_image_folder):
            os.makedirs(drone_image_folder)
        for idx, response in enumerate(responses):
            if response.compress: #png format
                print('image type {}, size {}'.format(
                    response.image_type, len(response.image_data_uint8)))
                filename = '{}\\{}-{}.png'.format(
                    drone_image_folder, image_id[drone_name], idx)
                image_id[drone_name] += 1
                airsim.write_file(filename, response.image_data_uint8)
                print('save image: {}'.format(filename))
            else:
                print('error: image format not support')
    return responses



def get_cur_pos(vehicle_name=''):
    cur_state = client.getMultirotorState(vehicle_name=vehicle_name)
    return cur_state.kinematics_estimated.position


def move_drone(drone_name, dx, dy, dz, yaw, speed):
    cur_pos = get_cur_pos(vehicle_name=drone_name)
    print('cur_pos:',cur_pos)
    next_pos = airsim.Vector3r(
         dx,  dy,  dz)
    print("try to move: {} -> {}, yaw={}, speed={}".format(
        cur_pos, next_pos, yaw, speed))

    t1 = time.time()
    thread = client.moveToPositionAsync(
        next_pos.x_val, next_pos.y_val, next_pos.z_val, speed,
        yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=yaw),
        drivetrain=airsim.DrivetrainType.MaxDegreeOfFreedom,
        vehicle_name=drone_name)
    time.sleep(8)
    thread.join()
    t2 = time.time()
    print('Time it takes:',t2-t1)
    cur_pos = get_cur_pos(vehicle_name=drone_name)
    print(cur_pos)



def control_drone1_move(is_stop):
    while Scenario!=0:

        if Scenario==1:
            try:
                move_drone('Drone1', 35, 10, -1.5, 90, 2.5)
            except RuntimeError as err:
                    time.sleep(1)
                    pass

            try:
                move_drone('Drone1', 10, 10, -1.5, 90, 2.5)

            except RuntimeError as err:
                    time.sleep(1)
                    pass

        if Scenario==2:
            try:
                move_drone('Drone1', 35, 10, -1.5, 90, 2.5)
            except RuntimeError as err:
                    time.sleep(1)
                    pass

            try:
                move_drone('Drone1', 10, 10, -1.5, 90, 2.5)

            except RuntimeError as err:
                    time.sleep(1)
                    pass

def control_drone1_pic(is_stop):

    i = 0
    while Scenario!=0:
        time.sleep(0.3)  # fps = 1
        # prevent RPC error stop the process
        print('take_picture')
        responses = None
        try:
            responses = take_picture('Drone1', is_save=False)
        except RPCError as err:
            print('RPCError due to two threads: {}'.format(err))
        except Exception as exp:
            print('Exception due to two threads: {}'.format(exp))
        except RuntimeError as err:
            print('RuntimeError due to two threads: {}'.format(err))


        if responses!=None:
            #sending image for inference
            image_data= responses[0].image_data_uint8
            data = base64.b64encode(image_data)
            #print('image is:',data)
            print('Sensing image for inference')
            result = dataflow.sendData(id='drone_image_data',data=data)
            print(i,':result is:',result)

        i = i+1




if __name__ == '__main__':

    # connect to the AirSim simulator
    client = airsim.MultirotorClient()
    client.confirmConnection()

    client.simEnableWeather(True)

    client.enableApiControl(True, "Drone1")
    client.armDisarm(True, "Drone1")

    f1 = client.takeoffAsync(vehicle_name="Drone1")
    f1.join()

    state1 = client.getMultirotorState(vehicle_name="Drone1")
    s = pprint.pformat(state1)
    print("state: %s" % s)


    #airsim.wait_key('Press any key to start workers')

    is_stop=False

    worker1 = threading.Thread(
        target=control_drone1_move, args=(is_stop,), name='control_drone1_move')
    worker2 = threading.Thread(
        target=control_drone1_pic, args=(is_stop,), name='control_drone1_pic')


    worker3 = threading.Thread(
        target=get_scenario, args=(), name='get_drone1_scenario')



    print('Start worker threads')
    worker1.start()
    worker2.start()
    worker3.start()

    print('Waiting for worker threads')
    worker2.join()
    worker1.join()
    worker3.join()

    #worker2.join()

    #airsim.wait_key('Press any key to reset to original state')
    client.armDisarm(False, "Drone1")
    client.reset()

    # that's enough fun for now. let's quit cleanly
    client.enableApiControl(False, "Drone1")
