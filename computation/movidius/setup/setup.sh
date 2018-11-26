wget -nc http://download.tensorflow.org/models/mobilenet_v1_2018_08_02/mobilenet_v1_1.0_224.tgz
tar -xvf mobilenet_v1_1.0_224.tgz

export PYTHONPATH="${PYTHONPATH}:/opt/movidius/caffe/python"

mvNCCompile -s 12 mobilenet_v1_1.0_224_frozen.pb -in=input -on=MobilenetV1/Predictions/Reshape_1


