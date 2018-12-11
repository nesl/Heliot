import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

from distutils.version import StrictVersion
from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
import json
import time


import cv2
PATH_TO_FROZEN_GRAPH = '../data/mobilenet_v2_1.4_224/mobilenet_v2_1.4_224_frozen.pb'

info='Time taken to load Model into memory:'
start_time=time.time()

detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')

end_time=time.time()
time_taken=end_time-start_time
print(info,time_taken)


# Load the labels

#Load categories
categories = []
with open('../data/' + 'categories.txt', 'r') as f:
    for line in f:
        cat = line.split('\n')[0]
        if cat != 'classes':
            categories.append(cat)
    f.close()
    print('Number of categories:', len(categories))


# Load image size
with open('../data/' + 'inputsize.txt', 'r') as f:
    reqsize = int(f.readline().split('\n')[0])
#print(reqsize)


#image_filename = '../data/' + 'image1.jpg'
def Load_and_process_img(image_filename):
    img = cv2.imread(image_filename)#.astype(numpy.float32)
    img = cv2.resize(img, (reqsize, reqsize))
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img = img.astype(float)

    #img values are scaled from -1 to 1
    img /= 255.0
    img -= 0.5
    img *= 2.0
    return img

sess=tf.Session(graph=detection_graph)


def run_inference_b1(key_name,image, graph,no_of_run):

    #model output layer name
    ops = graph.get_operations()
    all_tensor_names = {output.name for op in ops for output in op.outputs}
    #print(all_tensor_names)
    tensor_dict = {}
    for key in [key_name]:
        tensor_name = key + ':0'
        if tensor_name in all_tensor_names:
            tensor_dict[key] = graph.get_tensor_by_name(tensor_name)

    image=image.reshape(1,image.shape[0],image.shape[1],image.shape[2])
    image_tensor = graph.get_tensor_by_name('input:0')


    #Demo run, so that graph is loaded into TF memory
    sess.run(tensor_dict,feed_dict={image_tensor: image})


    # Run inference
    info='Time taken to run inference: run_inference_b1:'+str(no_of_run)+' Times: '
    start_time=time.time()

    for i in range(no_of_run):
        output_dict = sess.run(tensor_dict,
                          feed_dict={image_tensor: image})

    end_time=time.time()
    time_taken=end_time-start_time
    print(info,time_taken)

    #print(output_dict)
    top_inds = output_dict[key_name][0].argsort()[::-1][:5]

    result=[]
    for i in range(5):
        result.append([top_inds[i], categories[top_inds[i]], output_dict[key_name][0][top_inds[i]]])
    return result, time_taken



image_filename = '../data/' + 'Tiger.jpg'

img = Load_and_process_img(image_filename)

key_name='MobilenetV2/Predictions/Reshape_1'
result,time_taken=run_inference_b1(key_name,img,detection_graph,1000)

print('Time Taken to run Inference is:',time_taken)
print(result)
