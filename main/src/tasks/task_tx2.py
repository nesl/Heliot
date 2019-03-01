""" Object detection using Pretrained Tensorflow Model

Credits: This code is modified from the TensorFlow object detection tutorial available at:
https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb

"""


#Imports
import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import io

from distutils.version import StrictVersion
from collections import defaultdict
from io import StringIO
from PIL import Image
import base64
from base64 import decodestring
import json
import time

# Used to run RPC server
import msgpackrpc


# Utilities used
from utils import visualization_utils as vis_util
from utils.dataflow import *


if StrictVersion(tf.__version__) < StrictVersion('1.9.0'):
  raise ImportError('Please upgrade your TensorFlow installation to v1.9.* or later!')


# An inferencing image is saved with detection_boxes
save_image=True
download_model=False


# load image into numpy array
def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size

  try:
   image_np = np.array(image.getdata()).reshape(
      (im_height, im_width, 4)).astype(np.uint8)

  except:
   image_np = np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)


  image_np=image_np[:,:,:3]
  #print(image_np.shape)
  return image_np



# Running inference on single image
def run_inference_for_single_image(image, graph):
  # Get handles to input and output tensors

  image_tensor = graph.get_tensor_by_name('image_tensor:0')
  # Run inference
  output_dict = sess.run(tensor_dict,
                          feed_dict={image_tensor: np.expand_dims(image, 0)})

  # all outputs are float32 numpy arrays, so convert types as appropriate
  output_dict['num_detections'] = int(output_dict['num_detections'][0])
  output_dict['detection_classes'] = output_dict[
      'detection_classes'][0].astype(np.uint8)
  output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
  output_dict['detection_scores'] = output_dict['detection_scores'][0]
  if 'detection_masks' in output_dict:
    output_dict['detection_masks'] = output_dict['detection_masks'][0]
  return output_dict




def get_scores_labels(output_dict,confidence_limit):
    result=[]
    labels=[]
    detection_classes=output_dict['detection_classes']
    detection_scores=output_dict['detection_scores']
    for i in range(detection_classes.shape[0]):
        if detection_scores[i]>confidence_limit:
            result.append([category_index[str(detection_classes[i])],detection_scores[i]*100])
            labels.append(category_index[str(detection_classes[i])])
    return result,labels

class InferenceServer():

    @staticmethod
    def push(data):

        print('Image received')
        confidence_limit=0.3


        image_data = base64.b64decode(data)
        image = Image.open(io.BytesIO(image_data))
        image.save('inf_images/Image_received.png')

        #Converting to numpy array
        image_np = load_image_into_numpy_array(image)

        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        #image_np_expanded = np.expand_dims(image_np, axis=0)

        start_time=time.time()
        # Actual detection.
        output_dict = run_inference_for_single_image(image_np, detection_graph)
        end_time=time.time()
        time_taken=end_time-start_time
        print("Time Taken for Inference is:",time_taken)

        result,labels=get_scores_labels(output_dict,confidence_limit)

        if save_image:
            # The results of a detection is visualized
            vis_util.visualize_boxes_and_labels_on_image_array(
                image_np,
                output_dict['detection_boxes'],
                output_dict['detection_classes'],
                output_dict['detection_scores'],
                category_index,
                instance_masks=output_dict.get('detection_masks'),
                use_normalized_coordinates=True,
                line_thickness=8)
            im = Image.fromarray(image_np)
            #im.save('inf_images/Inference.jpg')

            if len(labels)>0:
                name=labels[0]
                if name =='car' or name =='person':
                    im.save('inf_images/'+name+'.jpg')





        print("Result is:",result)

        return labels
        #except Exception as inst:

if __name__ == "__main__":

	# #There is input port argument
	# if len(sys.argv)!=2:
	# 	print('usage: python3 main.py PORT_NUM')
	# 	print('Example: python3 main.py 18800')
	# 	exit(0)
	# #Parsing the input argument
	# port=int(sys.argv[1])

	"""
	The list of available modes:
	https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md
	"""
	# The model used for the inference
	MODEL_NAME = 'ssdlite_mobilenet_v2_coco_2018_05_09'#'ssd_mobilenet_v2_coco_2018_03_29'


	MODEL_FILE = MODEL_NAME + '.tar.gz'
	DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

	# Path to frozen detection graph. This is the actual model that is used for the object detection.
	PATH_TO_FROZEN_GRAPH = MODEL_NAME + '/frozen_inference_graph.pb'

	# Downloading the model, in case it is not present
	if download_model:
		opener = urllib.request.URLopener()
		opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
		tar_file = tarfile.open(MODEL_FILE)
		for file in tar_file.getmembers():
			file_name = os.path.basename(file.name)
			if 'frozen_inference_graph.pb' in file_name:
				tar_file.extract(file, os.getcwd())


	# Load a (frozen) Tensorflow model into memory.
	detection_graph = tf.Graph()
	with detection_graph.as_default():
	  od_graph_def = tf.GraphDef()
	  with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
	    serialized_graph = fid.read()
	    od_graph_def.ParseFromString(serialized_graph)
	    tf.import_graph_def(od_graph_def, name='')


	# Loading label map
	with open('data/labels.json') as f:
	    category_index = json.load(f)

		# TensorFlow Session
	sess=tf.Session(graph=detection_graph)

	ops = detection_graph.get_operations()
	all_tensor_names = {output.name for op in ops for output in op.outputs}
	  #print(all_tensor_names)
	tensor_dict = {}
	for key in ['num_detections', 'detection_boxes', 'detection_scores',
		    'detection_classes', 'detection_masks']:
	    tensor_name = key + ':0'
	    if tensor_name in all_tensor_names:
		    tensor_dict[key] = detection_graph.get_tensor_by_name(tensor_name)




		# Running one inference
	filepath = 'data/Im_rec.png'
	image = Image.open(filepath)
	image_np = load_image_into_numpy_array(image)

	res = run_inference_for_single_image(image_np, detection_graph)
	#print(res)
	print('*'*100)
	print('Available for Inference now')

	for i in range(1000):
	    data = dataflow.getData()
	    #print('Data is:',data)
	    InferenceServer.push(data)

	#print(res)
	#print(res)
	#print(res)

    # data = dataflow.getData()
    # print('Data is:',data)
    # InferenceServer.push(data)
