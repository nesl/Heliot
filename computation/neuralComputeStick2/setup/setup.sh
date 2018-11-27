
# Setting up the source variables
source /opt/intel/computer_vision_sdk/bin/setupvars.sh

# Downloading the model
python3 downloader.py --name googlenet-v2


# Optimizing the model for intel compute stick
mo.py --data_type FP16 --input_model classification/googlenet/v2/caffe/googlenet-v2.caffemodel --input_proto classification/googlenet/v2/caffe/googlenet-v2.prototxt


