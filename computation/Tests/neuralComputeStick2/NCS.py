
# source /opt/intel/computer_vision_sdk/bin/setupvars.sh

import sys
import os
import logging as log
import cv2
import numpy as np
from time import time
from openvino.inference_engine import IENetwork, IEPlugin


model_xml = '/home/nesl/Heliot/github/Heliot/computation/Tests/data/mobilenet_v1_1.0_224/mobilenet_v1_1.0_224_frozen.xml'
model_bin = '/home/nesl/Heliot/github/Heliot/computation/Tests/data/mobilenet_v1_1.0_224/mobilenet_v1_1.0_224_frozen.bin'

plugin = IEPlugin(device='MYRIAD', plugin_dirs=None)

net = IENetwork.from_ir(model=model_xml, weights=model_bin)

input_blob = next(iter(net.inputs))
out_blob = next(iter(net.outputs))

# Only one image as input
net.batch_size =1
n, c, h, w = net.inputs[input_blob].shape


def preprocess_input(x):
    x /= 255.0
    x -= 0.5
    x *= 2.0
    return x

def get_input_image(file_name):
    # Read and pre-process input images
    images = np.ndarray(shape=(n, c, h, w))
    #image = cv2.imread('data/Tiger.jpg')
    image = cv2.imread(file_name)

    #image = cv2.imread('data/image1.jpg')
    if image.shape[:-1] != (h, w):
        #print("Image is resized from {} to {}".format(image.shape[:-1], (h, w)))
        image = cv2.resize(image, (w, h))
    image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    image = image.astype(float)
    image = preprocess_input(image)
    image = image.transpose((2, 0, 1))  # Change data layout from HWC to CHW
    images[0] = image

    return images


def get_input_image(input_type):
    # Read and pre-process input images
    images = np.ndarray(shape=(n, c, h, w))

    image = np.ones((224, 224,3))
    if input_type=='ZERO':
        image=image*(0.0)

    if input_type=='ONE':
        image=image*(1.0)

    image = image.transpose((2, 0, 1))  # Change data layout from HWC to CHW
    images[0] = image

    return images


images= get_input_image('data/Tiger.jpg')

t0 = time()
# Loading model to the plugin
print("Loading model to the plugin")
exec_net = plugin.load(network=net)
res = exec_net.infer(inputs={input_blob: images})
t1 = time()

print('Total Time taken transfer model and to run Inference once is:', t1-t0)

del net


#t0 = time()
#res = exec_net.infer(inputs={input_blob: images})
#t1 = time()

#print('Time to run Inference is:', t1-t0)


#Load categories
categories = []
with open('../data/' + 'categories.txt', 'r') as f:
    for line in f:
        cat = line.split('\n')[0]
        if cat != 'classes':
            categories.append(cat)
    f.close()
    print('Number of categories:', len(categories))


############### Running the benchmark

def run_inference_b1(num_of_time=1):
    res=[]

    total_time_=0
    for j in range(1):
        start_time=time()
        for i in range(num_of_time):
            res = exec_net.infer()#We don't give input image now, running inference on previous input image
        end_time=time()
        print('Time to do inference: Times:',num_of_time,' : ',end_time-start_time)
        total_time_=total_time_+(end_time-start_time)


    #Verifying the inference results using last output
    # Processing output blob
    print("Processing output blob")
    res2 = res[out_blob]
    top_number = 5

    for i, probs in enumerate(res2):
        probs = np.squeeze(probs)

        top_ind = np.argsort(probs)[-top_number:][::-1]

        for id in top_ind:
            det_label = categories[id]  if categories else "#{}".format(id)
            print("{:.7f} label {}".format(probs[id], det_label))
        print("\n")

    print('run_inference_b1: Total time on inference is:',total_time_)

# A different image is loaded and moved to the compute stick
def run_inference_b2(num_of_time=1):
    res=[]

    total_time_=0
    for j in range(1):
        per_i_time=0
        for i in range(num_of_time):
            if i % 2==0:
                images= get_input_image('data/Tiger.jpg')
            else:
                images= get_input_image('data/image1.jpg')
            start_time=time()
            res= exec_net.infer(inputs={input_blob: images})
            end_time=time()
            per_i_time=per_i_time+end_time-start_time
        print('Time to do inference: Times:',num_of_time,' : ',per_i_time)
        total_time_=total_time_+per_i_time


    #Verifying the inference results using last output
    # Processing output blob
    print("Processing output blob")
    res2 = res[out_blob]
    top_number = 5

    for i, probs in enumerate(res2):
        probs = np.squeeze(probs)

        top_ind = np.argsort(probs)[-top_number:][::-1]

        for id in top_ind:
            det_label = categories[id]  if categories else "#{}".format(id)
            print("{:.7f} label {}".format(probs[id], det_label))
        print("\n")

    print('run_inference_b2: Total time on inference is:',total_time_)


## Running inference on ZERO or ONE image
def run_inference_b3(type, images,  num_of_time=1):
    res=[]
    res = exec_net.infer(inputs={input_blob: images})

    total_time_=0
    for j in range(1):
        start_time=time()
        for i in range(num_of_time):
            res = exec_net.infer()#We don't give input image now, running inference on previous input image
        end_time=time()
        print(type, ': Time to do inference: Times:',num_of_time,' : ',end_time-start_time)
        total_time_=total_time_+(end_time-start_time)


    #Verifying the inference results using last output
    # Processing output blob
    print("Processing output blob")
    res2 = res[out_blob]
    top_number = 5

    for i, probs in enumerate(res2):
        probs = np.squeeze(probs)

        top_ind = np.argsort(probs)[-top_number:][::-1]

        for id in top_ind:
            det_label = categories[id]  if categories else "#{}".format(id)
            print("{:.7f} label {}".format(probs[id], det_label))
        print("\n")

    print('run_inference_b1: Total time on inference is:',total_time_)


## Running on tiger
#run_inference_b1(1000)

#run_inference_b2(1000)



## Running on all ZERO
Type='ZERO'
images2= get_input_image(Type)
run_inference_b3(Type, images2,  num_of_time=1000)



## Running on all ZERO
Type='ONE'
images3= get_input_image(Type)
run_inference_b3(Type, images3,  num_of_time=1000)





del exec_net
del plugin