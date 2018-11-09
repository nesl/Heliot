#Making one module visible to another
import sys
sys.path.append('../')


from Slave import Slave
# importing the sensor module
from sensor.Sensor import Sensor
#importing the inference module
from computation.NN_inference import NN_inference


slave=Slave()


# Adding sensor to the slave
sensor = Sensor("Camera","Pi")
slave.setSensor(sensor)


# Printing sensor details
slave.printSensor()


# Adding inference to the slave
inference=NN_inference()
#Load a NN model in Keras
model_path='/media/sandeep/43f108db-7642-4e01-b534-59eca3dd838f/Research/vEdge/Trained_models/MNIST_model-1.h5'
from keras.models import load_model
model = load_model(model_path)
inference.initComputation(model)

slave.setCompute(inference)

# Printing inference details
#slave.printCompute()


#Setting up data for the slave
#Load MNIST data in keras
import keras
from keras.datasets import mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_test = x_test.reshape(10000, 784)
x_test = x_test.astype('float32')

slave.updateComputeData(x_test)
result=slave.runCompute()

print('*'*50)
print('*'*50)
print('Result size is:',result.shape)
print('*'*50)
