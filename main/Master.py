import rpyc
import sys
sys.path.append('../')


conn = rpyc.connect("localhost", 18861,config={"allow_all_attrs": True})

conn.root.initialize()

##Making a sample Compute
#importing the inference module
from computation.NN_inference import NN_inference

inference=NN_inference()
#Load a NN model in Keras
model_path='/media/sandeep/43f108db-7642-4e01-b534-59eca3dd838f/Research/vEdge/Trained_models/MNIST_model-1.h5'
from keras.models import load_model
model = load_model(model_path)
inference.initComputation(model)


##Adding MNIST model as compute to the Slave Device
conn.root.update_compute(inference)


##Loading the sample Test data
#Load MNIST data in keras
import keras
from keras.datasets import mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_test = x_test.reshape(10000, 784)
x_test = x_test.astype('float32')


##Adding the MNIST test data
conn.root.update_data(x_test)


conn.root.print_details()

res=conn.root.run_compute()
print('Res is:',res.shape)
print(res)
