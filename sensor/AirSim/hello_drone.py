'''
Modified from hello_drone.py code from AirSim github in the PythonClient folder
'''

import airsim

import numpy as np
import os
import tempfile
import pprint

#pos array
# Red Car is in between X=15 to 25. Y=0, Z=-3

pos=[
   [10, 0, -3],
   [15, 0, -3],
   [20, 0, -3],
   [25, 0, -3],
   [30, 0, -3]
]

pos=np.array(pos)

# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

# state = client.getMultirotorState()
# s = pprint.pformat(state)
# print("state: %s" % s)

#airsim.wait_key('Press any key to takeoff')
client.takeoffAsync().join()

pos_idx=0
#pos_idx = input('Enter the position index:')

while True:
    
    pos_idx=(pos_idx+1)%5
    print('Moving to position',pos[pos_idx])
    client.moveToPositionAsync(pos[pos_idx][0], pos[pos_idx][1], pos[pos_idx][2], 2).join()
    client.hoverAsync().join()

    # get camera images from the car
    responses = client.simGetImages([
        airsim.ImageRequest("0", airsim.ImageType.Scene)#scene vision image in png format
        ]) 

    print('Retrieved images: %d' % len(responses))

    tmp_dir = os.path.join(tempfile.gettempdir(), "airsim_drone")
    print ("Saving images to %s" % tmp_dir)
    try:
        os.makedirs(tmp_dir)
    except OSError:
        if not os.path.isdir(tmp_dir):
            raise

    for idx, response in enumerate(responses):

        filename = os.path.join(tmp_dir, str(idx))

        if response.pixels_as_float:
            print("Type %d, size %d" % (response.image_type, len(response.image_data_float)))
            airsim.write_pfm(os.path.normpath(filename + '.pfm'), airsim.get_pfm_array(response))
        elif response.compress: #png format
            print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
            airsim.write_file(os.path.normpath(filename + '.png'), response.image_data_uint8)
        else: #uncompressed array
            print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
            img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8) #get numpy array
            img_rgba = img1d.reshape(response.height, response.width, 4) #reshape array to 4 channel image array H X W X 4
            img_rgba = np.flipud(img_rgba) #original image is flipped vertically
            img_rgba[:,:,1:2] = 100 #just for fun add little bit of green in all pixels
            airsim.write_png(os.path.normpath(filename + '.greener.png'), img_rgba) #write to png



client.armDisarm(False)
client.reset()

# that's enough fun for now. let's quit cleanly
client.enableApiControl(False)
